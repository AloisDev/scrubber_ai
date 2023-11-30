from ast import List
import asyncio
import json
import logging
import httpx
from constants import GOOGLE_ADDRESS_VALIDATION_URL, GOOGLE_API_KEY
from schemas import Document


async def validate_address(document: Document):
    url = GOOGLE_ADDRESS_VALIDATION_URL
    headers = {
        "content-type": "application/json",
    }
    params = {"key": GOOGLE_API_KEY}

    mapped_address_list = await map_address(document)

    current_delay = 0.1  # Set the initial retry delay to 100ms.
    max_delay = 5  # Set the maximum retry delay to 5 seconds.

    for mapped_address in mapped_address_list:
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url,
                        headers=headers,
                        params=params,
                        data=json.dumps(mapped_address),
                    )
                    response.raise_for_status()
            except httpx.RequestError as exc:
                logging.error(
                    f"An error occurred while requesting {exc.request.url!r}."
                )
            else:
                google_response = response.json()

                if google_response:
                    logging.info(
                        google_response["result"]["address"]["addressComponents"]
                    )
                    validation_result = await validate_address_components(
                        google_response["result"]["address"]["addressComponents"]
                    )
                    return validation_result
                else:
                    raise Exception("error")

            if current_delay > max_delay:
                raise Exception("Too many retry attempts.")

            logging.info(f"Waiting {current_delay}, seconds before retrying.")

            await asyncio.sleep(current_delay)
            current_delay *= 2


async def map_address(document: Document) -> List:
    address_list = []
    mapped_address_list = []

    patient_address = document.Patient
    address_list.append(patient_address)

    # if (
    #     "Insurance" in document
    #     and document["Insurance"][0]["relationshipToPatient"] != "self"
    # ):
    #     address_list.extend(document["Insurance"])

    # logging.info(
    #     "address_list", address_list
    # )  # deberia tener todos los objetos con las direcciones

    for address in address_list:
        address_lines = []
        address_lines.extend([address.street, address.streetExtended])
        # if address["street"] and address["streetExtended"]:
        #     address_lines.extend([address["street"], address["streetExtended"]])
        # else:
        #     address_lines.extend([address["insuranceCompanyAddress"]])

        mapped_address = {
            "address": {
                "regionCode": address.countryCode if address.countryCode else "US",
                "postalCode": address.postCode
                if address.postCode
                else address.insuranceCompanyZip,
                "administrativeArea": address.state,
                "locality": address.city,
                "addressLines": address_lines,
            }
        }

        mapped_address_list.append(mapped_address)
    return mapped_address_list


async def add_insurance_address():
    return "Not implemented yet"


async def validate_address_components(components_list: list) -> str:
    not_confirmed_components = []
    for component in components_list:
        if component["confirmationLevel"] != "CONFIRMED":
            not_confirmed_components.append(component)

    if len(not_confirmed_components) == 0:
        return "Pass"
    else:
        # create record in db with failed validation and hl7 details
        return "Fail"
