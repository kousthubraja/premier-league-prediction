set -e
python script1_fetch_train_data.py
python script_2_clean_train_data.py
python script_3_push_data_to_db.py
python script_4_make_model.py
python script_5_predict.py
