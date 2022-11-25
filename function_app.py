'''Base Function App file'''
import azure.functions as func

from services import UserService

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name(name="IsThisWorking")
@app.route(route="test", methods=[func.HttpMethod.GET])
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    '''Test Function'''
    user = UserService.from_request(req)

    return func.HttpResponse(
        f"Hello, {user.name}. This HTTP triggered function executed successfully.")
