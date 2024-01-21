import grpc
import idm_service_pb2
import idm_service_pb2_grpc

class IDMClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = idm_service_pb2_grpc.IDMServiceStub(self.channel)

    def login(self, username, password):
        request = idm_service_pb2.LoginRequest(username=username, password=password)
        return self.stub.Login(request)

    def register(self, username, email, password):
        request = idm_service_pb2.RegisterRequest(username=username, email=email, password=password)
        return self.stub.Register(request)

    def get_user(self, user_id):
        request = idm_service_pb2.GetUserRequest(id=user_id)
        return self.stub.GetUser(request)

    def update_user(self, user_id, email, password, is_active):
        request = idm_service_pb2.UpdateUserRequest(id=user_id, email=email, password=password, is_active=is_active)
        return self.stub.UpdateUser(request)

    def delete_user(self, user_id):
        request = idm_service_pb2.DeleteUserRequest(id=user_id)
        return self.stub.DeleteUser(request)
    
def main():
    client = IDMClient()
    
    # Example usage
    # response = client.login(username="example", password="password")
    # print("Login Response:", response)

    response = client.register(username="newuser", email="newuser@example.com", password="password")
    print("Register Response:", response)

    # Add more calls as needed

if __name__ == '__main__':
    main()
