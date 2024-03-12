from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from faker import Faker
import requests

app = FastAPI()
faker = Faker()

def generate_random_data(count):
    data = []
    for _ in range(count):
        name = faker.name()
        address = faker.address()
        email = faker.email()
        phone_number = faker.phone_number()
        birthdate = faker.date_of_birth().strftime("%Y-%m-%d")
        job = faker.job()
        credit_card = faker.credit_card_number(card_type="mastercard")
        
        api_url = "https://randomuser.me/api/"
        response = requests.get(api_url)
        user_data = response.json().get("results", [])[0]
        
        avatar_url = user_data.get("picture", {}).get("large", "")
        
        data.append({
            "name": name,
            "address": address,
            "email": email,
            "phone_number": phone_number,
            "birthdate": birthdate,
            "job": job,
            "credit_card": credit_card,
            "avatar_url": avatar_url
        })
    return data

@app.get("/", response_class=HTMLResponse)
def read_Data(count: int = Query(default=0, ge=0, le=100)):
    data_list = generate_random_data(count)

    html_content = f"""
    <html>
        <head>
            <title>Informacion Personal</title>
            <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2621/2621824.png" type="image/x-icon">
            <style>
                body {{ background: lightblue url("https://fondosmil.com/fondo/37944.jpg") no-repeat fixed center;  margin: 0; padding: 0; font-family: "Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif; color: #fff}}
                .datacontainer {{ width: 600px; margin: 5em auto; padding: 20px; border-radius: 1em; text-align: center; }}
                .datadiv {{ width: 600px; margin: 5em auto; padding: 20px; background-color: #fff; border-radius: 1em; text-align: center; color: #000}}
                form {{ margin-bottom: 20px; }}
                img {{ border-radius: 50%; margin-bottom: 10px; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ margin-bottom: 10px; }}
                a:link, a:visited {{ color: #38488f; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class = "datacontainer">
                <h1>Informacion personal de facebook</h1>
                <form action="/" method="get">
                    <label for="cantidad">Cantidad de Informacion:</label>
                    <input type="number" id="cantidad" name="count" value="{count}" min="0" max="100">
                    <button type="submit">Nueva informacion</button>
                </form>
                {"".join(
                    f"""
                    <div class= "datadiv"; style="border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                        <img src="{data['avatar_url']}" alt="{data['name']}" style="width: 150px; height: 150px;">
                        <ul>
                            <li><strong>Nombre:</strong> {data['name']}</li>
                            <li><strong>Dirección:</strong> {data['address']}</li>
                            <li><strong>Correo Electrónico:</strong> {data['email']}</li>
                            <li><strong>Número de Teléfono:</strong> {data['phone_number']}</li>
                            <li><strong>Fecha de Nacimiento:</strong> {data['birthdate']}</li>
                            <li><strong>Trabajo:</strong> {data['job']}</li>
                            <li><strong>Tarjeta de Crédito:</strong> {data['credit_card']}</li>
                        </ul>
                    </div>
                    """
                    for data in data_list
                )}
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
