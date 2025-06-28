from fastapi import APIRouter, Depends
from surprise import Dataset, Reader, SVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sqlmodel import Session,select
from app.database import get_session
from app.models import Restaurant,Menu,Food,Users,Orders


rec = APIRouter(prefix="")

@rec.post("/recommendation")
def recomm(user_id:int,session:Session = Depends(get_session) ):
    fud_df = pd.read_csv("C:\\Swiggy clone\\food.csv")
    menu_df = pd.read_csv("C:\\Swiggy clone\\menu.csv")
    order_df = pd.read_csv("C:\\Swiggy clone\\orders.csv")
    user_df = pd.read_csv("C:\\Swiggy clone\\users.csv")
    rest_df = pd.read_csv("C:\\Swiggy clone\\restaurant.csv")
    order_df.rename(columns={
        'user_id':'u_id'
    }, inplace=True)
    menu_df.rename(columns={
        'r_id':'m_r_id',
        'f_id':'m_f_id'
    }, inplace=True)

    df1 = menu_df.merge(fud_df, left_on='m_f_id', right_on='f_id', how='inner', suffixes=('', '_food'))
    df2 = df1.merge(rest_df, left_on='m_r_id', right_on='id', how='inner', suffixes=('', '_rest'))
    df3 = df2.merge(order_df, left_on='id', right_on='r_id', how='inner', suffixes=('', '_order'))
    df = df3.merge(user_df, left_on='u_id', right_on='user_id', how='inner', suffixes=('', '_user'))
    df.drop(['cuisine', "order_date", "sales_qty", 'sales_amount', 'currency','Age', 'Gender', 'Marital Status','Occupation','Country','link','menu_id'], axis=1, inplace=True)
    df['rating'] = df['rating'].replace('--', 0)
    df[0:10000]

    def combine_columns(df, cols):
        features = []  
        for i in range(df.shape[0]):
            to_add = ""  
            for j in range(len(cols)):
                to_add += str(df[cols[j]][i]) + ' '
            features.append(to_add)
        return features  

    df.reset_index(drop=True, inplace=True)
    df1 = df.iloc[:10000].copy()
    df1['combined'] = combine_columns(df1, df1.columns.tolist())

    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df1['combined'])
    cosine_similarities = cosine_similarity(tfidf_matrix)
    def get_content_based_recommendations(user_id, top_n):
        user_index = df1[df1['user_id'] == user_id].index[0]
        scores = list(enumerate(cosine_similarities[user_index]))
        scores = sorted(scores, key=lambda x:x[1], reverse=True)
        scores = scores[1:]
        mv =[]
        for i in scores[:top_n]:
            mv.append(df1.loc[i[0], ['user_id', 'o_id', 'm_id']])
        return mv
    # mv = get_content_based_recommendations(25858, 10)
    # mv_dicts = [row.to_dict() for row in mv]
    # print(mv_dicts)

    df2 = df1.copy(deep=True)
    df2.reset_index(drop=True, inplace=True)
    df2['o_id&m_id_combined'] = combine_columns(df2, ['o_id','m_id'])
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df2[['user_id','o_id&m_id_combined','rating']], reader)

    algo = SVD()
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    def get_collaborative_filtering_recommendations(user_id, top_n):
        testset = trainset.build_anti_testset()
        testset = filter(lambda x: x[0] == user_id, testset)
        predictions = algo.test(testset)
        predictions.sort(key=lambda x: x.est, reverse=True)
        recommendations = [prediction.iid for prediction in predictions[:top_n]]
        return recommendations
    # colla = get_collaborative_filtering_recommendations(76202,30)
    # collabrative =[{'o_id': int(x.split()[0]), 'm_id': int(x.split()[1])} for x in colla]
    # print(collabrative)

    def get_hybrid_recommendations(user_id, top_n):
        content_based_recommendations = get_content_based_recommendations(user_id, top_n)
        collaborative_filtering_recommendations = get_collaborative_filtering_recommendations(user_id, top_n)
        content_based_ids = [str(item['m_id']) for item in content_based_recommendations]
        collaborative_filtering_ids = [str(item.split()[1]) for item in collaborative_filtering_recommendations]
        hybrid_ids = list(set(content_based_ids + collaborative_filtering_ids))
        hybrid_dicts = []
        for m_id in hybrid_ids[:top_n]:
            hybrid_dicts.append({
                'user_id': user_id,
                'm_id': int(m_id),
            })
        return hybrid_dicts
    # user_id = 27999
    # top_n = 10
    recommendations = get_hybrid_recommendations(user_id, 5)

    details = []
    for rec_item in recommendations:
        m_id = rec_item["m_id"]
        # Get menu item from DB
        menu_stmt = select(Menu).where(Menu.m_id == m_id)
        menu = session.exec(menu_stmt).first()
        food_stmt = select(Food).where(Food.f_id == menu.f_id)
        restaurant_stmt = select(Restaurant).where(Restaurant.id == menu.r_id)
        
        food = session.exec(food_stmt).first()
        restaurant = session.exec(restaurant_stmt).first()
        details.append({
            "menu_id": m_id,
            "food_item": food.item,
            "veg_or_non_veg": food.veg_or_non_veg,
            "price": menu.price,
            "cuisine": menu.cuisine,
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "city": restaurant.city,
                "address": restaurant.address,
                "rating": restaurant.rating,
            }
        })
    return {"message":"restaurant menu recommendation","data":details,"errorcode":0}