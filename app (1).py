import streamlit as st
from sqlalchemy import text

list_category = ['', 'Health', 'Sport and outdors', 'Furniture', 'Clothing and Apparel', 'Beauty and personal care', 'Books and Literature', 'Electronic', 'Automotive', 'Home and Kitchen Appliance', 'Toys']
list_discounted = ['', 'Yes', 'No']
list_ratings = ['', 1, 2, 3, 4, 5]

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://arsenhakim:RC7muUaFB6YJ@ep-sparkling-lake-52449485.us-east-2.aws.neon.tech/web")

st.header('Simple Product Data Management System')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT id, product_name, category, brand, price, discounted, ratings_1_to_5, supplier_name FROM produk ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    with conn.session as session:
        if st.button('Tambah Data'):
            query = text('INSERT INTO produk (product_name, category, brand, price, discounted, ratings_1_to_5, supplier_name) VALUES (:1, :2, :3, :4, :5, :6, :7);')
            session.execute(query, {'1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': ''})
            session.commit()

        data = conn.query('SELECT id, product_name, category, brand, price, discounted, ratings_1_to_5, supplier_name FROM produk ORDER By id;', ttl="0")
        for _, result in data.iterrows():        
            id = result['id']
            product_name_lama = result["product_name"]
            category_lama = result["category"]
            brand_lama = result["brand"]
            price_lama = result["price"]
            discounted_lama = result["discounted"]
            ratings_1_to_5_lama = result["ratings_1_to_5"]
            supplier_name_lama = result["supplier_name"]

            with st.expander(f'a.n. {product_name_lama}'):
                with st.form(f'data-{id}'):
                    product_name_baru = st.text_input("product_name", product_name_lama)
                    category_baru = st.selectbox("category", list_category, index=[c.lower() for c in list_category].index(category_lama.lower()) if category_lama and category_lama.lower() in [c.lower() for c in list_category] else 0 if category_lama else None)
                    brand_baru = st.text_input("brand", brand_lama)
                    price_baru = st.text_input("price", price_lama)
                    discounted_baru = st.selectbox("discounted", list_discounted, list_discounted.index(discounted_lama) if discounted_lama and discounted_lama in list_discounted else 0)
                    ratings_1_to_5_baru = st.selectbox("ratings_1_to_5", list_ratings, list_ratings.index(ratings_1_to_5_lama) if ratings_1_to_5_lama and ratings_1_to_5_lama in list_ratings else 0)
                    supplier_name_baru = st.text_input("supplier_name", supplier_name_lama)
                    
                    col1, col2 = st.columns([1, 6])

                    with col1:
                        if st.form_submit_button('UPDATE'):
                            query = text('UPDATE produk \
                                          SET product_name=:1, category=:2, brand=:3, price=:4, \
                                          discounted=:5, ratings_1_to_5=:6, supplier_name=:7 \
                                          WHERE id=:8;')
                            session.execute(query, {'1': product_name_baru, '2': category_baru, '3': brand_baru, '4': price_baru, 
                                                    '5': discounted_baru, '6': ratings_1_to_5_baru, '7': supplier_name_baru, '8': id})
                            session.commit()
                            st.experimental_rerun()
                    
                    with col2:
                        if st.form_submit_button('DELETE'):
                            query = text(f'DELETE FROM produk WHERE id=:1;')
                            session.execute(query, {'1': id})
                            session.commit()
                            st.experimental_rerun()
