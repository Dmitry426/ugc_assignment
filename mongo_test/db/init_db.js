const dbName = "test_mongo";
const conn = new Mongo();
const db = conn.getDB(dbName);

const collectionSettings = [
    {
        name: "likes",
        indexFields: [
            {'movie_id': -1},
            {'user_id': -1},
            {'movie_id': -1, 'value': -1},
            {'user_id': -1, 'value': -1},
        ],
        uniqueFields: [
            {'movie_id': 1, 'user_id': 1}
        ]
    },
    {
        name: "reviews",
        indexFields: [
            {'user_id': -1},
            {'movie_id': -1}
        ],
        uniqueFields: [
            {'movie_id': 1, 'user_id': 1}
        ]
    },
    {
        name: "bookmarks",
        indexFields: [
            {'user_id': -1},
            {'movie_id': -1}
        ],
        uniqueFields: [
            {'movie_id': 1, 'user_id': 1}
        ]
    }
];

collectionSettings.forEach((collection) => {
    const collectionName = collection.name;
    const indexFields = collection.indexFields;
    const uniqueFields = collection.uniqueFields;

    db.createCollection(collectionName);
    if (indexFields !== undefined) {
        indexFields.forEach((field) => {
            db[collectionName].createIndex(field);
        })
    }

    if (uniqueFields !== undefined) {
        uniqueFields.forEach((field) => {
            db[collectionName].createIndex(field, {"unique" : true});
        })
    }
});
