# import os
# import random
# from datetime import datetime, timedelta
# from typing import Dict, List, Optional
# from uuid import UUID, uuid4

# from dotenv import load_dotenv

# from app.models import (
#     AccessDevice,
#     Blog,
#     BlogComment,
#     BlogRequest,
#     Forum,
#     Language,
#     Product,
#     ProductLanContent,
#     ProductRequest,
#     ResourceAccess,
#     Role,
#     Thread,
#     ThreadComment,
#     User,
# )

# load_dotenv()

# BLOB_URL = os.getenv("BLOB_URL")


# # Base de datos simulada
# class Database:
#     users: Dict[UUID, User] = {}
#     products: Dict[UUID, Product] = {}
#     blogs: Dict[UUID, Blog] = {}
#     blog_comments: Dict[UUID, BlogComment] = {}
#     product_requests: Dict[UUID, ProductRequest] = {}
#     blog_requests: Dict[UUID, BlogRequest] = {}
#     resource_accesses: List[ResourceAccess] = []
#     forums: Dict[str, Forum] = {}
#     threads: Dict[UUID, Thread] = {}
#     thread_comments: Dict[UUID, ThreadComment] = {}

#     # Para autenticación
#     user_tokens: Dict[str, UUID] = {}
#     user_likes: Dict[UUID, List[UUID]] = {}  # usuario_id -> [comentario_id, ...]

#     @classmethod
#     def generate_token(cls, user_id: UUID) -> str:
#         token = f"mock-token-{uuid4()}"
#         cls.user_tokens[token] = user_id
#         return token

#     @classmethod
#     def get_user_by_token(cls, token: str) -> Optional[User]:
#         if token in cls.user_tokens:
#             user_id = cls.user_tokens[token]
#             return cls.users.get(user_id)
#         return None


# # Crear datos mock iniciales
# def create_mock_data():
#     # Crear usuarios
#     admin = User(
#         id=uuid4(),
#         email="admin@example.com",
#         nickName="admin",
#         role=Role.EMPLOYEE,
#         image="https://randomuser.me/api/portraits/men/1.jpg",
#         isBloqued=False,
#         creationDate=datetime.now() - timedelta(days=30),
#     )

#     user1 = User(
#         id=uuid4(),
#         email="user1@example.com",
#         nickName="user1",
#         role=Role.USER,
#         image="https://randomuser.me/api/portraits/women/1.jpg",
#         isBloqued=False,
#         creationDate=datetime.now() - timedelta(days=25),
#     )

#     user2 = User(
#         id=uuid4(),
#         email="user2@example.com",
#         nickName="user2",
#         role=Role.USER,
#         image="https://randomuser.me/api/portraits/men/2.jpg",
#         isBloqued=True,
#         creationDate=datetime.now() - timedelta(days=20),
#     )

#     # Añadir usuarios a la base de datos
#     Database.users[admin.id] = admin
#     Database.users[user1.id] = user1
#     Database.users[user2.id] = user2

#     # Crear productos
#     product1_id = uuid4()
#     product1_content_es = ProductLanContent(
#         lan=Language.ES,
#         name="Aceite de oliva virgen",
#         description="Aceite de oliva virgen extra de la mejor calidad",
#     )
#     product1_content_en = ProductLanContent(
#         lan=Language.EN,
#         name="Virgin olive oil",
#         description="Extra virgin olive oil of the highest quality",
#     )
#     product1 = Product(
#         id=product1_id,
#         image=f"{BLOB_URL}/aceite-oliva.png",
#         regions=["ES-AN", "ES-CM"],
#         productLanContents=[product1_content_es, product1_content_en],
#         creationDate=datetime.now() - timedelta(days=15),
#     )

#     product2_id = uuid4()
#     product2_content_es = ProductLanContent(
#         lan=Language.ES, name="Jamón ibérico", description="Jamón ibérico de bellota"
#     )
#     product2 = Product(
#         id=product2_id,
#         image=f"{BLOB_URL}/jamon-iberico.jpg",
#         regions=["ES-EX", "ES-AN"],
#         productLanContents=[product2_content_es],
#         creationDate=datetime.now() - timedelta(days=10),
#     )

#     # Añadir productos a la base de datos
#     Database.products[product1.id] = product1
#     Database.products[product2.id] = product2

#     # Crear blogs
#     blog1_id = uuid4()
#     blog1 = Blog(
#         id=blog1_id,
#         product=product1,
#         lan=Language.ES,
#         title="El aceite de oliva en la dieta mediterránea",
#         description="Beneficios del aceite de oliva en la dieta mediterránea",
#         image=f"{BLOB_URL}/aceite-oliva.png",
#         creationDate=datetime.now() - timedelta(days=5),
#     )

#     blog2_id = uuid4()
#     blog2 = Blog(
#         id=blog2_id,
#         product=product2,
#         lan=Language.ES,
#         title="Proceso de curación del jamón ibérico",
#         description="Detalles del proceso de curación del jamón ibérico de bellota",
#         image=f"{BLOB_URL}/jamón-ibérico.jpg",
#         creationDate=datetime.now() - timedelta(days=3),
#     )

#     # Añadir blogs a la base de datos
#     Database.blogs[blog1.id] = blog1
#     Database.blogs[blog2.id] = blog2

#     # Crear comentarios para blogs
#     comment1_id = uuid4()
#     comment1 = BlogComment(
#         id=comment1_id,
#         blogId=blog1_id,
#         user=user1,
#         comment="¡Me encantó este artículo!",
#         nLikes=5,
#         creationDate=datetime.now() - timedelta(days=2),
#     )

#     comment2_id = uuid4()
#     comment2 = BlogComment(
#         id=comment2_id,
#         blogId=blog1_id,
#         user=user2,
#         comment="Muy informativo",
#         image="https://example.com/images/comment2.jpg",
#         nLikes=3,
#         creationDate=datetime.now() - timedelta(days=1),
#     )

#     # Añadir comentarios a la base de datos y a los blogs
#     Database.blog_comments[comment1.id] = comment1
#     Database.blog_comments[comment2.id] = comment2

#     blog1.comments.append(comment1)
#     blog1.comments.append(comment2)

#     # Crear solicitudes de productos
#     prod_req1_id = uuid4()
#     prod_req1 = ProductRequest(
#         id=prod_req1_id,
#         name="Queso manchego",
#         user=user1,
#         description="Queso manchego con denominación de origen",
#         image="https://example.com/images/prodreq1.jpg",
#         creationDate=datetime.now() - timedelta(days=8),
#     )

#     # Añadir solicitudes de productos a la base de datos
#     Database.product_requests[prod_req1.id] = prod_req1

#     # Crear solicitudes de blogs
#     blog_req1_id = uuid4()
#     blog_req1 = BlogRequest(
#         id=blog_req1_id,
#         user=user1,
#         title="Maridaje del jamón ibérico",
#         description="Ideas para maridar jamón ibérico con vinos",
#         product=product2,
#         image="https://example.com/images/blogreq1.jpg",
#         creationDate=datetime.now() - timedelta(days=7),
#     )

#     # Añadir solicitudes de blogs a la base de datos
#     Database.blog_requests[blog_req1.id] = blog_req1

#     # Crear registros de acceso a recursos
#     for i in range(10):
#         user = random.choice([admin, user1, user2])
#         access = ResourceAccess(
#             id=uuid4(),
#             userId=user.id,
#             resourceType="BLOG",
#             resourceId=random.choice([blog1_id, blog2_id]),
#             accessType="READ",
#             accessDate=datetime.now() - timedelta(days=i, hours=random.randint(0, 23)),
#             deviceType=random.choice([AccessDevice.WEB, AccessDevice.MOBILE]),
#         )
#         Database.resource_accesses.append(access)

#     # Crear foros (regiones)
#     regions = [
#         ("ES-AN", "Andalucía"),
#         ("ES-AR", "Aragón"),
#         ("ES-AS", "Asturias"),
#         ("ES-CN", "Canarias"),
#         ("ES-CM", "Castilla-La Mancha"),
#         ("ES-CL", "Castilla y León"),
#         ("ES-CT", "Cataluña"),
#         ("ES-EX", "Extremadura"),
#         ("ES-GA", "Galicia"),
#         ("ES-IB", "Islas Baleares"),
#         ("ES-RI", "La Rioja"),
#         ("ES-MD", "Madrid"),
#         ("ES-MC", "Murcia"),
#         ("ES-NC", "Navarra"),
#         ("ES-PV", "País Vasco"),
#         ("ES-VC", "Valenciana"),
#     ]

#     for region_id, region_name in regions:
#         Database.forums[region_id] = Forum(regionId=region_id, regionName=region_name)

#     # Crear hilos de discusión
#     thread1_id = uuid4()
#     thread1 = Thread(
#         id=thread1_id,
#         regionId="ES-AN",
#         lan=Language.ES,
#         title="Mejores aceites de Andalucía",
#         description="Discusión sobre los mejores aceites de oliva de Andalucía",
#         creationDate=datetime.now() - timedelta(days=4),
#     )

#     thread2_id = uuid4()
#     thread2 = Thread(
#         id=thread2_id,
#         regionId="ES-EX",
#         lan=Language.ES,
#         title="Productores de jamón en Extremadura",
#         description="Lista de productores de jamón en Extremadura",
#         creationDate=datetime.now() - timedelta(days=2),
#     )

#     # Añadir hilos de discusión a la base de datos
#     Database.threads[thread1.id] = thread1
#     Database.threads[thread2.id] = thread2

#     # Crear comentarios para hilos
#     thread_comment1 = ThreadComment(
#         id=uuid4(),
#         threadId=thread1_id,
#         user=user1,
#         content="Recomiendo el aceite de la cooperativa de Baena",
#         creationDate=datetime.now() - timedelta(days=3, hours=12),
#     )

#     thread_comment2 = ThreadComment(
#         id=uuid4(),
#         threadId=thread1_id,
#         user=admin,
#         content="Los aceites de Priego de Córdoba son excelentes",
#         creationDate=datetime.now() - timedelta(days=3),
#     )

#     # Añadir comentarios a la base de datos y a los hilos
#     Database.thread_comments[thread_comment1.id] = thread_comment1
#     Database.thread_comments[thread_comment2.id] = thread_comment2

#     thread1.comments.append(thread_comment1)
#     thread1.comments.append(thread_comment2)

#     # Simular tokens para usuarios (para uso en autenticación)
#     Database.user_tokens["admin-token"] = admin.id
#     Database.user_tokens["user1-token"] = user1.id
#     Database.user_tokens["user2-token"] = user2.id
