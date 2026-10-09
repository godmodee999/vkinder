import vk_api

user_token = ''
vk_session = vk_api.VkApi(token=user_token)
vk = vk_session.get_api()


def search_users(age, gender, city):
    result = vk.users.search(
        age_from=age,
        age_to=age,
        sex=gender,
        city=city,
        has_photo=1,
        count=100,
        fields="city, bdate"
    )

    candidates = []

    for user in result["items"]:
        if user["is_closed"] is False:
            candidates.append({
                "id": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"]
            })

    return candidates

def get_photos(user_id):
    result=[]
    likes_list=[]
    photos = vk.photos.get(owner_id=user_id,count=20, album_id="profile", extended=1)
    for a in photos["items"]:
        likes_list.append((a["likes"]["count"], a["id"]))
    sort = sorted(likes_list, key=lambda x: x[0], reverse=True)[:3]
    for i in sort:
        result.append(i[1])
    return result

import requests

response = requests.get(
    "https://api.vk.com/method/users.get",
    params={
        "access_token": user_token,
        "v": "5.199"
    }
)

print(response.json())