import httpx
from fastapi import HTTPException, status

CITY_SERVICE_URL = "http://127.0.0.1:8002/cities"

async def verify_city_exists(city_id: int):
    try:
        async with httpx.AsyncClient() as client:
            url = f"{CITY_SERVICE_URL}/{city_id}"
            print("URL CONSULTADA:", url)
            response = await client.get(url)

            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La ciudad asociada no existe"
                )

            if 400 <= response.status_code < 500:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error desde microservicio de ciudades: {response.text}"
                )

            if response.status_code >= 500:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="El microservicio de ciudades está fallando"
                )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo alcanzar el microservicio de ciudades"
        )
