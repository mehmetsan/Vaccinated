import typing as tp
from api.models import Vaccination


def get_all_vaccinations() -> tp.List:
    vaccinations = Vaccination.objects.all()
    results = []

    for vaccination in vaccinations:
        results.append({
            'id': vaccination.id,
            'name': vaccination.name,
            "dose": vaccination.dose,
            "start": vaccination.start,
            "end": vaccination.end,
            "optional": "true" if vaccination.optional else "false",
            "total_doses": vaccination.total_doses,
            "display_name": str(vaccination)
        })
    return results
