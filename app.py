import datetime
from sklearn.metrics import mean_squared_error
import pandas as pd
from flask import jsonify, request
from sklearn.model_selection import train_test_split
from werkzeug.security import check_password_hash, generate_password_hash
from static.gradient import GradientBoostingRegressor
from static.schemas import modelS
from static.models import db, MODELS, app
import random

o_key = "CgFuhy@g9XBc-6NEqTZ2ESUUc-6Z*SppVR#Nua"


@app.route('/gradient/start/', methods=['GET', 'POST'])
async def gradientstart():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify({'data': 0})
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify({'data': 0})
    if operation_key['data'] == 'start':
        MODELS.query.delete()
        data = pd.read_csv('flats_moscow.csv', index_col=0).drop('code', axis=1)
        data = data.dropna()
        X = data.drop('price', axis=1)
        y = data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.12, random_state=42)
        gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        gb.fit(X_train, y_train)
        df_x = pd.DataFrame(columns=X_test.columns)
        df_y = pd.DataFrame(columns=['price'])
        for i in range(25):
            rn = random.randint(0, len(X_test) - 1)
            df_x.loc[i] = X_test.iloc[rn]
            df_y.loc[i] = y_test.iloc[rn]

        X_test = df_x
        y_test = df_y
        y_pred = gb.predict(X_test)

        for i in range(len(X_test)):
            db.session.add(
                MODELS(price=int(y_test.to_numpy(dtype='float64')[i][0]),
                       totsp=X_test['totsp'].to_numpy(dtype='float64')[i],
                       dist=X_test['dist'].to_numpy(dtype='float64')[i],
                       metrdist=X_test['metrdist'].to_numpy(dtype='float64')[i],
                       walk=X_test['walk'].to_numpy(dtype='float64')[i], pred=int(y_pred[i]),
                       error=int(y_test.to_numpy(dtype='float64')[i][0]) - int(y_pred[i])))
        db.session.commit()
        return jsonify({'data': 1})

    return jsonify({'data': 0})


@app.route('/gradient/print/', methods=['GET', 'POST'])
async def gradientprint():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify({'data': 0})
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify({'data': 0})
    return jsonify(modelS(many=True).dump(MODELS.query.all()))


if __name__ == '__main__':
    app.run(host="127.0.0.3", port=8000)
