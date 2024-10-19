
import requests
import pandas as pd
import matplotlib.pyplot as plt

def getToken() -> str:
    try:
        file = open("./.token")
        token = file.read()
    except:
        raise Exception("Fallo al adquirir el token")
    finally:
        file.close()
    
    return token

if __name__== "__main__":
    print("API BCRA")

    endpoint = "https://api.estadisticasbcra.com/usd"
    token = getToken()

    print("Endpoint: ", endpoint)
    
    response = requests.get(endpoint, headers={"Authorization": "BEARER " + token})

    print("Response: ", response)

    if not response.ok:
        print("Error!")
        exit(1)

    response_json = response.json()
    df = pd.DataFrame(response_json)
    df["d"] = pd.to_datetime(df["d"], errors="coerce")
    df["v"] = pd.to_numeric(df["v"], errors="coerce").astype("float")

    print(df)

    start="2000"
    end="2024"
    df2 = df[df["d"].isin(pd.date_range(start=start, end=end, freq="1D"))]

    print(df2)
    
    plt.title("Dolar desde {} a {}".format(start, end))
    plt.xlabel("Año-Mes")
    plt.ylabel("Cotización del dolar en pesos argentinos")
    plt.plot(df2["d"], df2["v"])
    plt.show()
