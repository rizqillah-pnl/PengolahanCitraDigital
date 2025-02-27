import time
import base64
from datetime import datetime
import cv2
import pytesseract
from pytesseract import Output
from pytesseract import image_to_string
from flask_cors import CORS
import PIL.Image as Image
import io

from flask import Flask, render_template, request, jsonify, json, make_response
import sys

app = Flask(__name__)
cors = CORS(app)


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@app.route('/api', methods=['POST'])
def api():
    res = json.loads(request.data).get('gambar')
    res = res.split("base64,")
    gambar = base64.b64decode(res[1])
    img = Image.open(io.BytesIO(gambar))
    output = dict()

    image = img.crop((120, 45, 300, 150))

    a = pytesseract.image_to_string(image)

    b = dict()
    b['bank'] = a
    b['bank'] = b['bank'].replace('\n', ' ')

    if (b['bank'] == "BANK SYARIAH INDONESIA "):
        image = img.crop((75, 175, 640, 220))
        d = pytesseract.image_to_string(image)

        for b in d.splitlines():
            b = b.split(' ')

        d = b[0] + " " + b[1]

        if (d == "Transfer Bank" or d == "Transfer Antar"):

            # image = img[250:850, 75:640]
            image = img.crop((75, 250, 640, 850))
            roi = [
                [(5, (11 + 23)), (82, 640), 'status', 'text'],
                [(66, (71 + 23)), (200, 640), 'nomor_transaksi', 'text'],
                [(95, (100 + 28)), (206, 640), 'tgl', 'tanggal'],
                [(156, (161 + 23)), (155, 640), 'nomor_struk', 'text'],
                [(245, (250 + 28)), (108, 640), 'pengirim', 'text'],
                [(336, (341 + 23)), (150, 640), 'no_rekening_tujuan', 'text'],
                [(365, (370 + 24)), (179, 640), 'bank_penerima', 'text'],
                [(395, (400 + 24)), (120, 640), 'nama_penerima', 'text'],
                [(455, (460 + 24)), (126, 640), 'jumlah', 'number']
            ]

            for x, r in enumerate(roi):
                imgCrop = image.crop((r[1][0], r[0][0], r[1][1], r[0][1]))

                text = pytesseract.image_to_string(imgCrop)

                if r[3] == 'text':
                    output[r[2]] = text.replace("\n", "")
                if r[3] == 'number':
                    output[r[2]] = int(
                        ((text.replace("\n", "")).replace(".", "")).replace(",", ""))
                if r[3] == 'tanggal':
                    text = datetime.strptime(
                        ((text.replace("\n", "")).replace(" a", "")), "%d %b %Y %H:%M:%S")
                    output[r[2]] = text

            return jsonify(output)

        elif (d == "Pembayaran/Pembelian ShopeePay"):

            # image = img[250:850, 75:640]
            image = img.crop((75, 250, 640, 850))

            roi = [
                [(10, (16 + 28)), (90, 640), 'status', 'text'],
                [(79, (84 + 26)), (218, 640), 'no_transaksi', 'text'],
                [(113, (118 + 26)), (222, 640), 'tgl', 'tanggal'],
                [(181, (186 + 26)), (170, 640), 'no_struk', 'text'],
                [(283, (288 + 26)), (168, 640), 'jns_pembelian', 'text'],
                [(317, (322 + 26)), (239, 640), 'no_hp', 'text'],
                [(385, (390 + 26)), (168, 640), 'reference', 'text'],
                [(419, (424 + 26)), (144, 640), 'nominal', 'number'],
                [(453, (458 + 26)), (160, 640), 'fee', 'number'],
                [(487, (492 + 26)), (220, 640), 'total', 'number']
            ]

            for x, r in enumerate(roi):
                imgCrop = image.crop((r[1][0], r[0][0], r[1][1], r[0][1]))

                text = pytesseract.image_to_string(imgCrop)

                if r[3] == 'text':
                    output[r[2]] = text.replace("\n", "")
                if r[3] == 'number':
                    output[r[2]] = int(((text.replace("\n", "")).replace(
                        ".", "")).replace(",", "").replace("Rp", ""))
                if r[3] == 'tanggal':
                    data = text.replace(";", "")
                    text = data.replace("\n", "")
                    text = datetime.strptime((text), "%d %b%Y%H:%M:%S")
                    output[r[2]] = text

            return jsonify(output)

        elif (d == "Pembayaran/Pembelian OVO"):

            # image = img[250:850, 75:640]
            image = img.crop((75, 250, 640, 850))

            roi = [
                [(5, (11 + 23)), (82, 640), 'status', 'text'],
                [(66, (71 + 23)), (200, 640), 'nomor_transaksi', 'text'],
                [(95, (100 + 28)), (206, 640), 'tgl', 'tanggal'],
                [(156, (161 + 23)), (155, 640), 'nomor_struk', 'text'],
                [(245, (250 + 28)), (150, 640), 'jenis_pembelian', 'text'],
                [(280, (285 + 23)), (210, 640), 'no_pelanggan', 'text'],
                [(310, (315 + 23)), (245, 640), 'nama_pelanggan', 'text'],
                [(336, (341 + 26)), (165, 640), 'nilai_topup', 'number'],
                [(395, (400 + 24)), (238, 640), 'total_bayar', 'number']
            ]

            for x, r in enumerate(roi):
                imgCrop = image.crop((r[1][0], r[0][0], r[1][1], r[0][1]))

                text = pytesseract.image_to_string(imgCrop)

                if r[3] == 'text':
                    output[r[2]] = text.replace("\n", "")
                if r[3] == 'number':
                    output[r[2]] = int(((text.replace("\n", "")).replace(
                        ".", "")).replace(",", "").replace("Rp", ""))
                if r[3] == 'tanggal':
                    text = datetime.strptime(
                        ((text.replace("\n", "")).replace(" a", "")), "%d %b %Y %H:%M:%S")
                    output[r[2]] = text

            return jsonify(output)

        elif (d == "Pembayaran/Pembelian Go"):

            # image = img[250:850, 75:640]
            image = img.crop((75, 250, 640, 850))

            roi = [
                [(5, (11 + 23)), (82, 640), 'status', 'text'],
                [(66, (71 + 23)), (200, 640), 'nomor_transaksi', 'text'],
                [(95, (100 + 28)), (206, 640), 'tgl', 'tanggal'],
                [(156, (161 + 23)), (155, 640), 'nomor_struk', 'text'],
                [(245, (250 + 28)), (180, 640), 'jenis_pembayaran', 'text'],
                [(280, (285 + 23)), (219, 640), 'no_handphone', 'text'],
                [(310, (315 + 23)), (230, 640), 'nama_costumer', 'text'],
                [(336, (341 + 23)), (150, 640), 'admin_fee', 'number'],
                [(365, (370 + 24)), (220, 640), 'nominal_topup', 'number'],
                [(395, (400 + 24)), (120, 640), 'no_reff', 'text'],
                [(427, (431 + 24)), (195, 640), 'total_bayar', 'number']
            ]

            for x, r in enumerate(roi):
                imgCrop = image.crop((r[1][0], r[0][0], r[1][1], r[0][1]))

                text = pytesseract.image_to_string(imgCrop)

                if r[3] == 'text':
                    output[r[2]] = text.replace("\n", "")
                if r[3] == 'number':
                    output[r[2]] = int(((text.replace("\n", "")).replace(
                        ".", "")).replace(",", "").replace("Rp", ""))
                if r[3] == 'tanggal':
                    text = datetime.strptime(
                        ((text.replace("\n", "")).replace(" a", "")), "%d %b %Y %H:%M:%S")
                    output[r[2]] = text

            return jsonify(output)

        elif (d == "Pembayaran/Pembelian DANA"):

            # image = img[250:850, 75:640]
            image = img.crop((75, 250, 640, 850))

            roi = [
                [(6, (11 + 23)), (82, 640), 'status', 'text'],
                [(66, (71 + 23)), (201, 560), 'no_transaksi', 'text'],
                [(90, (100 + 28)), (204, 560), 'tgl', 'tanggal'],
                [(155, (160 + 24)), (154, 560), 'no_struk', 'text'],
                [(246, (251 + 23)), (157, 640), 'jns_pembelian', 'text'],
                [(276, (281 + 23)), (90, 640), 'no_hp', 'text'],
                [(306, (311 + 23)), (243, 560), 'nama', 'text'],
                [(336, (341 + 25)), (170, 640), 'jumlah', 'number'],
                [(396, (401 + 23)), (0, 640), 'order_id', 'text'],
                [(425, (430 + 24)), (175, 640), 'transaksi_id', 'text'],
                [(456, (461 + 25)), (199, 560), 'total', 'number']

            ]

            for x, r in enumerate(roi):
                imgCrop = image.crop((r[1][0], r[0][0], r[1][1], r[0][1]))

                text = pytesseract.image_to_string(imgCrop)

                if r[3] == 'text':
                    output[r[2]] = text.replace("\n", "")
                if r[3] == 'number':
                    output[r[2]] = int(((text.replace("\n", "")).replace(
                        ".", "")).replace(",", "").replace("Rp", ""))
                if r[3] == 'tanggal':
                    text = datetime.strptime(
                        ((text.replace("\n", "")).replace(" a", "")), "%d %b %Y %H:%M:%S")
                    output[r[2]] = text
            return jsonify(output)

    else:
        print("Permintaan ditolak, keluar dari proses!")


app.run(debug=True)
