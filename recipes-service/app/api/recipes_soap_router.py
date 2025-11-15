import xml.etree.ElementTree as ET

from fastapi import APIRouter, HTTPException, Request, Response, status

from app.domain import services
from app.domain.models import RecipeCreate

router = APIRouter(
    prefix="/recipes/soap",
    tags=["recipes-soap"],
)

SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"
NSMAP = {"soap": SOAP_NS}


def build_soap_envelope(inner: ET.Element) -> str:
    """Envuelve el body en un Envelope SOAP estándar."""
    envelope = ET.Element(f"{{{SOAP_NS}}}Envelope")
    body = ET.SubElement(envelope, f"{{{SOAP_NS}}}Body")
    body.append(inner)
    xml_bytes = ET.tostring(envelope, encoding="utf-8", xml_declaration=True)
    return xml_bytes.decode("utf-8")


def parse_soap_body(raw_xml: bytes) -> ET.Element:
    """Devuelve el elemento dentro de soap:Body."""
    try:
        root = ET.fromstring(raw_xml)
    except ET.ParseError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid XML payload",
        )

    body = root.find("soap:Body", NSMAP)
    if body is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing SOAP Body",
        )

    # Esperamos un único hijo dentro de Body (CreateRecipeRequest o ListRecipesRequest)
    if len(body) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty SOAP Body",
        )

    return body[0]  # primer elemento dentro del Body


@router.post(
    "/create",
    response_class=Response,
    summary="Crear receta (SOAP/XML)",
)
async def create_recipe_soap(request: Request) -> Response:
    """
    SOAP endpoint para crear una receta.

    Espera algo como:
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <CreateRecipeRequest>
          <Name>...</Name>
          <Steps>...</Steps>
        </CreateRecipeRequest>
      </soap:Body>
    </soap:Envelope>
    """
    raw_xml = await request.body()
    inner = parse_soap_body(raw_xml)

    if inner.tag != "CreateRecipeRequest":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expected CreateRecipeRequest in SOAP Body",
        )

    name_el = inner.find("Name")
    steps_el = inner.find("Steps")

    if name_el is None or not (name_el.text and name_el.text.strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Name element",
        )

    name = name_el.text.strip()
    steps = steps_el.text.strip() if (steps_el is not None and steps_el.text) else None

    recipe = services.create_recipe(RecipeCreate(name=name, steps=steps))

    resp = ET.Element("CreateRecipeResponse")
    ET.SubElement(resp, "Id").text = str(recipe.id)
    ET.SubElement(resp, "Name").text = recipe.name
    ET.SubElement(resp, "Steps").text = recipe.steps or ""

    xml_response = build_soap_envelope(resp)
    return Response(content=xml_response, media_type="text/xml")


@router.post(
    "/list",
    response_class=Response,
    summary="Listar recetas (SOAP/XML)",
)
async def list_recipes_soap(request: Request) -> Response:
    """
    SOAP endpoint para listar recetas.

    Espera:
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <ListRecipesRequest/>
      </soap:Body>
    </soap:Envelope>
    """
    raw_xml = await request.body()
    inner = parse_soap_body(raw_xml)

    if inner.tag != "ListRecipesRequest":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expected ListRecipesRequest in SOAP Body",
        )

    recipes = services.get_all_recipes()

    resp = ET.Element("ListRecipesResponse")
    recipes_el = ET.SubElement(resp, "Recipes")

    for r in recipes:
        r_el = ET.SubElement(recipes_el, "Recipe")
        ET.SubElement(r_el, "Id").text = str(r.id)
        ET.SubElement(r_el, "Name").text = r.name
        ET.SubElement(r_el, "Steps").text = r.steps or ""

    xml_response = build_soap_envelope(resp)
    return Response(content=xml_response, media_type="text/xml")