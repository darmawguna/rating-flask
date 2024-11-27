import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
import msgpack
from flask import Response


review_endpoints = Blueprint('books', __name__)

# Endpoint untuk membaca semua review
@review_endpoints.route('/', methods=['GET'])
def read():
    # Membuat koneksi ke database
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query untuk mendapatkan daftar buku
    select_query = "SELECT * FROM reviews"
    cursor.execute(select_query)
    results = cursor.fetchall()
    
    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()
    
    # Mengembalikan respons dalam format JSON
    return jsonify({"message": "OK", "datas": results}), 200


# Endpoint untuk membaca review berdasarkan ID review
@review_endpoints.route('/<int:id_review>', methods=['GET'])
def read_by_id(id_review):
    # Membuat koneksi ke database
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query untuk mendapatkan review berdasarkan id_review
    select_query = "SELECT * FROM reviews WHERE id_review = %s"
    cursor.execute(select_query, (id_review,))
    result = cursor.fetchone()
    
    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()

    if result:
        return jsonify({"message": "OK", "data": result}), 200
    else:
        return jsonify({"message": "Review not found"}), 404


# Endpoint untuk menambahkan review baru
@review_endpoints.route('/create', methods=['POST'])
def create():
    # Mendapatkan data dari request
    data = request.get_json()
    
    # Validasi input form (harus ada id_film, review, dan rating)
    if not data or not data.get('id_film') or not data.get('review') or not data.get('rating'):
        return jsonify({"message": "Missing required fields"}), 400

    id_film = data['id_film']
    review = data['review']
    rating = data['rating']
    
    # Membuat koneksi ke database
    connection = get_connection()
    cursor = connection.cursor()
    
    # Query untuk menyimpan review baru
    insert_query = "INSERT INTO reviews (id_film, review, rating) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (id_film, review, rating))
    connection.commit()

    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Review created successfully"}), 201


# Endpoint untuk mengupdate review berdasarkan ID review
@review_endpoints.route('/update/<int:id_review>', methods=['PUT'])
def update(id_review):
    # Mendapatkan data dari request
    data = request.get_json()
    
    # Validasi input form (harus ada review dan rating)
    if not data or not data.get('review') or not data.get('rating'):
        return jsonify({"message": "Missing required fields"}), 400

    review = data['review']
    rating = data['rating']
    
    # Membuat koneksi ke database
    connection = get_connection()
    cursor = connection.cursor()
    
    # Query untuk mengupdate review berdasarkan id_review
    update_query = "UPDATE reviews SET review = %s, rating = %s WHERE id_review = %s"
    cursor.execute(update_query, (review, rating, id_review))
    connection.commit()
    
    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Review updated successfully"}), 200


# Endpoint untuk menghapus review berdasarkan ID review
@review_endpoints.route('/delete/<int:id_review>', methods=['DELETE'])
def delete(id_review):
    # Membuat koneksi ke database
    connection = get_connection()
    cursor = connection.cursor()
    
    # Query untuk menghapus review berdasarkan id_review
    delete_query = "DELETE FROM reviews WHERE id_review = %s"
    cursor.execute(delete_query, (id_review,))
    connection.commit()
    
    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()

    return jsonify({"message": "Review deleted successfully"}), 200


@review_endpoints.route('/film/<int:id_film>', methods=['GET'])
def get_review_by_film(id_film):
    # Membuat koneksi ke database
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Query untuk mendapatkan rating dan review berdasarkan id_film
    select_query = "SELECT review, rating FROM reviews WHERE id_film = %s"
    cursor.execute(select_query, (id_film,))
    results = cursor.fetchall()

    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()

    # Mengecek jika ada hasil
    if results:
        # Mengemas hasil dengan msgpack
        msgpack_data = msgpack.packb({"message": "OK", "reviews": results})
        return Response(msgpack_data, content_type='application/x-msgpack', status=200)
    else:
        # Mengembalikan response error dengan msgpack
        msgpack_data = msgpack.packb({"message": "No reviews found for this movie."})
        return Response(msgpack_data, content_type='application/x-msgpack', status=404)
