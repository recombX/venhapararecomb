from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.infra.sqlalchemy.reposipories import nfe_repository
from app.infra.sqlalchemy.reposipories import person_repository
from app.infra.sqlalchemy.reposipories import address_repository


def get_nfe(db: Session, nfe_id: str) -> dict:
    """Function responsible for obtaining information regarding the NFe and returning it formatted.
    Args:
        db (Session): database session

    Returns:
        dict: Returns all information regarding an NFe.
    """
    nfe = nfe_repository.get_nfe_by_nfe_id(db, nfe_id)

    if(not nfe):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "this document does not exist."}
        )

    provider = person_repository.get_person(db, nfe.provider_id)
    client = person_repository.get_person(db, nfe.client_id)
    address_pro = address_repository.get_address_by_person_id(
        db, nfe.provider_id)
    address_cli = address_repository.get_address_by_person_id(
        db, nfe.client_id)

    add_prov = schemas.AddressView(
        id=address_pro.id,
        logradouro=address_pro.logradouro,
        numero=address_pro.numero,
        bairro=address_pro.bairro,
        municipio=address_pro.municipio,
        uf=address_pro.uf,
        cep=address_pro.cep,
        pais=address_pro.pais
    )
    add_cli = schemas.AddressView(
        id=address_cli.id,
        logradouro=address_cli.logradouro,
        numero=address_cli.numero,
        bairro=address_cli.bairro,
        municipio=address_cli.municipio,
        uf=address_cli.uf,
        cep=address_cli.cep,
        pais=address_cli.pais
    )
    per_cli = schemas.PersonView(
        id=client.id,
        name=client.name,
        cpf=client.cpf,
        cnpj=client.cnpj,
        address=add_cli,
    )
    per_prov = schemas.PersonView(
        id=provider.id,
        name=provider.name,
        cpf=provider.cpf,
        cnpj=provider.cnpj,
        address=add_prov,
    )
    data = schemas.NFeView(
        id=nfe.id,
        nfe_id=nfe.nfe_id,
        date_venc=nfe.date_venc,
        total=nfe.total,
        provider=per_prov,
        client=per_cli,
    )

    return data


def get_all_nfe(db: Session) -> List[dict]:
    """Function responsible for getting the information already formatted regarding the NFe and returning them.

    Args:
        db (Session): database session

    Returns:
        List[dict]: returns a list with all information for all NFe.
    """
    nfes = nfe_repository.get_all_nfe(db)
    lst = []
    for nfe in nfes:
        lst.append(get_nfe(db, nfe.nfe_id))
    data = reversed(lst)
    return data
