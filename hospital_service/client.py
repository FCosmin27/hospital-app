import grpc
import idm_service_pb2
import idm_service_pb2_grpc

class IDMClient:
    def __init__(self, host='idm_service', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = idm_service_pb2_grpc.IDMServiceStub(self.channel)
        
    def get_user(self, user_id):
        request = idm_service_pb2.GetUserRequest(id=user_id)
        return self.stub.GetUser(request)