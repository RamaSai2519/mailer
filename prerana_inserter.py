from config import prusers_collection
import pandas

file = 'paid.csv'

data = pandas.read_csv(file)
data_dicts = data.to_dict(orient='records')

for record in data_dicts:
    user = {
        'name': record['Name'],
        'email': record['Email'],
        'phoneNumber': record['Mobile'],
        'gitamite': True
    }

    result = prusers_collection.update_one(
        {'email': user['email']},
        {'$setOnInsert': user},
        upsert=True
    )

    if result.matched_count != 0:
        print(f"Skipped duplicate email: {user['email']}")

print(f"Processed {len(data_dicts)} records")
