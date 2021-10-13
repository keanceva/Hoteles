from administracion.models import Publicidad

#Funcion que carga todas las publicidades para ponerlas en templates de la app reserva
def add_variable_to_context(request):

    anuncios = Publicidad.objects.all()

    return {
        'anuncios':anuncios,
    }