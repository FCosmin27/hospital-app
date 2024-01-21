import grpc
from concurrent import futures
import idm_service_pb2
import idm_service_pb2_grpc
import crud, schemas, security, models
from database import engine, get_db, delete_tables, insert_roles_into_table, insert_admin_user

#Uncommnet to delete tables
#delete_tables()

models.Base.metadata.create_all(bind=engine)

#Uncommnet at first run
insert_roles_into_table() 
insert_admin_user()

class IDMServiceServicer(idm_service_pb2_grpc.IDMServiceServicer):
    def Login(self, request, context):
        db = get_db()
        try:
            user = crud.authenticate_user(db, request.username, request.password)
            
            if not user:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details('Invalid username or password')
                return idm_service_pb2.LoginResponse()
            
            access_token = security.create_access_token({"sub": user.username, "role": user.role.name})
            context.set_code(grpc.StatusCode.OK)
            context.set_details('Login successful')
            return idm_service_pb2.LoginResponse(token=access_token)
        
        finally:
            db.close()
    
    def Register(self, request, context):
        db = get_db()
        try:
            user_create = schemas.UserCreate(username=request.username, email=request.email, password=request.password)
            user = crud.create_user(db, user_create, "patient")
            if not user:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details('User already exists')
                return idm_service_pb2.RegisterResponse()
            
            context.set_code(grpc.StatusCode.OK)
            context.set_details('Registration successful')
            return idm_service_pb2.RegisterResponse(id=user.id)
        finally:
            db.close()
            
    def GetUser(self, request, context):
        db = get_db()
        try: 
            user = crud.get_user(db, request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('User not found')
                return idm_service_pb2.UserResponse()
            context.set_code(grpc.StatusCode.OK)
            context.set_details('User found')
            return idm_service_pb2.UserResponse(id=user.id, username=user.username, email=user.email, is_active=user.is_active)
        finally:
            db.close()
       
    def UpdateUser(self, request, context):
        db = get_db()
        try:
            user_update = schemas.UserUpdate(email=request.email, password=request.password, is_active=request.is_active)
            user = crud.update_user(db, request.id, user_update)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('User not found')
                return idm_service_pb2.UserResponse()
            context.set_code(grpc.StatusCode.OK)
            context.set_details('User updated')
            return idm_service_pb2.UserResponse(id=user.id, username=user.username, email=user.email, is_active=user.is_active)
        finally:
            db.close()
            
    def DeleteUser(self, request, context):
        db = get_db()
        try:
            user = crud.delete_user(db, request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('User not found')
                return idm_service_pb2.DeleteUserResponse()
            context.set_code(grpc.StatusCode.OK)
            context.set_details('User deleted')
            return idm_service_pb2.DeleteUserResponse(message="User deleted")
        finally:
            db.close()
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    idm_service_pb2_grpc.add_IDMServiceServicer_to_server(IDMServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
