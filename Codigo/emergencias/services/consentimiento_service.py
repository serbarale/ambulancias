from ..dao.consentimiento_dao import FormatoConsentimientoDAO

class FormatoConsentimientoService:
    @staticmethod
    def registrar_consentimiento(datos):
        if not datos.get("nombre_paciente") or not datos.get("dni_paciente") or not datos.get("personal_medico"):
            raise ValueError("Faltan campos obligatorios.")
        return FormatoConsentimientoDAO.crear(datos)

    @staticmethod
    def obtener_consentimiento(informe_id):
        return FormatoConsentimientoDAO.obtener_por_informe(informe_id)
