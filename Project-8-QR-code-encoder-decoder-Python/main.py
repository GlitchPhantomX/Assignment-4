import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

def create_qr_code(data, filename, fill_color="black", back_color="white"):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(filename)
        print(f"✅ QR code generated and saved as {filename}")
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")

def decode_qr_code(filename):
    try:
        img = Image.open(filename)
        decoded_objects = decode(img)
        if not decoded_objects:
            print("⚠️ No QR code detected in the image.")
            return None

        decoded_data_list = [obj.data.decode('utf-8') for obj in decoded_objects]
        print("✅ Decoded Data:")
        for i, data in enumerate(decoded_data_list, 1):
            print(f"{i}. {data}")
        return decoded_data_list
    except Exception as e:
        print(f"❌ Error decoding QR code: {e}")

if __name__ == "__main__":
    data = input("Enter the data for the QR code: ") or "https://www.example.com"
    filename = input("Enter the filename (with .png extension): ") or "example_qr.png"
    
    fill_color = input("Enter foreground color (default: black): ") or "black"
    back_color = input("Enter background color (default: white): ") or "white"

    create_qr_code(data, filename, fill_color, back_color)
    decode_qr_code(filename)
