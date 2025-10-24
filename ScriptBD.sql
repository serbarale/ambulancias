BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ambulancias_ambulancia" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "placa" varchar(10) NOT NULL UNIQUE, "estado" varchar(20) NOT NULL, "tipo_A" varchar(10) NOT NULL, "marca" varchar(50) NOT NULL, "fecha_adquisicion" date NOT NULL);
CREATE TABLE IF NOT EXISTS "ambulancias_avería" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tipoF" varchar(10) NOT NULL, "descripcion_averia" text NOT NULL, "fecha_reporte" date NOT NULL, "nombre_colaborador" varchar(100) NOT NULL, "ambulancia_id" bigint NOT NULL REFERENCES "ambulancias_ambulancia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "ambulancias_combustible" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fecha_combustible" date NOT NULL, "comb_inicial" integer NOT NULL, "comb_final" integer NOT NULL, "km_inicial" integer NOT NULL, "km_final" integer NOT NULL, "nombre_colaborador" varchar(100) NOT NULL, "ambulancia_id" bigint NOT NULL REFERENCES "ambulancias_ambulancia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "emergencias_formatoconsentimiento" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "lugar" varchar(100) NOT NULL, "nombre_paciente" varchar(100) NOT NULL, "dni_paciente" varchar(12) NOT NULL, "personal_medico" varchar(100) NOT NULL, "acepta_acto_medico" bool NOT NULL, "acepta_traslado" bool NOT NULL, "fecha_firma" date NOT NULL, "informe_id" bigint NOT NULL UNIQUE REFERENCES "emergencias_informeemergencia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "emergencias_formatorevocacion" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre_declarante" varchar(100) NOT NULL, "tipo_persona" varchar(20) NOT NULL, "tipo_documento" varchar(20) NOT NULL, "numero_documento" varchar(20) NOT NULL, "motivo_revocacion" text NOT NULL, "nombre_testigo" varchar(100) NOT NULL, "fecha_firma" date NOT NULL, "informe_id" bigint NOT NULL UNIQUE REFERENCES "emergencias_informeemergencia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "emergencias_informeemergencia" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "direccion" varchar(255) NOT NULL, "prioridad" varchar(10) NOT NULL, "fecha_registro" datetime NOT NULL, "estado" varchar(20) NOT NULL, "nombre_chofer" varchar(100) NOT NULL, "paciente_opcional" varchar(100) NULL, "ambulancia_id" bigint NOT NULL REFERENCES "ambulancias_ambulancia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "emergencias_insumoutilizado" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer NOT NULL, "insumo_id" bigint NOT NULL REFERENCES "inventarios_insumomedico" ("id") DEFERRABLE INITIALLY DEFERRED, "reporte_id" bigint NOT NULL REFERENCES "emergencias_reporteemergencia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "emergencias_reporteemergencia" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "procedimientos" text NOT NULL, "pertenencias" text NOT NULL, "fecha_registro" datetime NOT NULL, "informe_id" bigint NOT NULL UNIQUE REFERENCES "emergencias_informeemergencia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "emergencias_reportepaciente" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "paciente_id" bigint NOT NULL REFERENCES "pacientes_paciente" ("id") DEFERRABLE INITIALLY DEFERRED, "reporte_id" bigint NOT NULL REFERENCES "emergencias_reporteemergencia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "inventarios_checklist" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre_colaborador" varchar(100) NOT NULL, "fecha_registro" datetime NOT NULL, "ambulancia_id" bigint NOT NULL REFERENCES "ambulancias_ambulancia" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "inventarios_detallechecklist" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad_contada" integer NOT NULL, "checklist_id" bigint NOT NULL REFERENCES "inventarios_checklist" ("id") DEFERRABLE INITIALLY DEFERRED, "insumo_id" bigint NOT NULL REFERENCES "inventarios_insumomedico" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "inventarios_insumomedico" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(100) NOT NULL, "stock" integer NOT NULL, "unidadMedida" varchar(20) NOT NULL, "tipoAmbulancia" varchar(10) NOT NULL);
CREATE TABLE IF NOT EXISTS "pacientes_historialmedico" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "alergias" text NULL, "tipoSangre" varchar(5) NOT NULL, "enfermedades" text NULL, "paciente_id" bigint NOT NULL UNIQUE REFERENCES "pacientes_paciente" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "pacientes_paciente" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(50) NOT NULL, "apellido" varchar(50) NOT NULL, "dni" varchar(8) NOT NULL UNIQUE, "direccion" varchar(200) NULL, "email" varchar(100) NULL, "telefono" varchar(15) NULL, "fechaNacimiento" date NOT NULL, "sexo" varchar(20) NOT NULL);
INSERT INTO "ambulancias_ambulancia" ("id","placa","estado","tipo_A","marca","fecha_adquisicion") VALUES (1,'ABC-123','en_proceso','tipo_3','Mercedes-Benz','2025-06-01'),
 (2,'XYZ-345','preparada','tipo_3','Nissan','2025-06-24'),
 (3,'FXO-340','inhabilitada','tipo_2','Toyota','2025-06-11'),
 (4,'GTH-049','preparada','tipo_3','Ford','2025-06-06'),
 (5,'RHY-493','preparada','tipo_1','Mercedes-Benz','2025-06-01'),
 (6,'RGU-293','inhabilitada','tipo_2','Nissan','2025-05-01'),
 (7,'QYH-381','preparada','tipo_3','Toyota','2025-04-03'),
 (8,'QI0-E34','en_proceso','tipo_1','Ford','2025-06-10');
INSERT INTO "ambulancias_avería" ("id","tipoF","descripcion_averia","fecha_reporte","nombre_colaborador","ambulancia_id") VALUES (1,'critico','Falla del sistema eléctrico principal','2025-06-24','Juan Pérez López',1),
 (2,'leve','Luces de emergencia intermitentes','2025-06-24','Carlos Sánchez Castro',2),
 (3,'grave','Problema de frenos','2025-06-24','Pedro Ramírez Soto',3),
 (4,'critico','Error en el monitor de signos vitales','2025-06-24','Juan Pérez López',4),
 (5,'leve','Puerta trasera no cierra herméticamente','2025-06-24','Pedro Ramírez Soto',6),
 (6,'grave','Fuga menor de líquido de dirección','2025-06-24','Ana Torres Vega',7),
 (7,'critico','fallo en la sirena','2025-06-24','Ana Torres Vegas',6);
INSERT INTO "ambulancias_combustible" ("id","fecha_combustible","comb_inicial","comb_final","km_inicial","km_final","nombre_colaborador","ambulancia_id") VALUES (1,'2025-06-18',36,15,12500,12750,'Juan Pérez López',1),
 (2,'2025-06-24',41,29,15320,15400,'Carlos Sánchez Castro',7),
 (3,'2025-06-15',14,32,1300,1350,'Pedro Ramírez Soto',6),
 (4,'2025-06-01',47,44,10203,13003,'Juan Pérez López',6),
 (5,'2025-06-05',45,36,2344,2400,'Carlos Sánchez Castro',5);
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Can add log entry'),
 (2,1,'change_logentry','Can change log entry'),
 (3,1,'delete_logentry','Can delete log entry'),
 (4,1,'view_logentry','Can view log entry'),
 (5,2,'add_permission','Can add permission'),
 (6,2,'change_permission','Can change permission'),
 (7,2,'delete_permission','Can delete permission'),
 (8,2,'view_permission','Can view permission'),
 (9,3,'add_group','Can add group'),
 (10,3,'change_group','Can change group'),
 (11,3,'delete_group','Can delete group'),
 (12,3,'view_group','Can view group'),
 (13,4,'add_user','Can add user'),
 (14,4,'change_user','Can change user'),
 (15,4,'delete_user','Can delete user'),
 (16,4,'view_user','Can view user'),
 (17,5,'add_contenttype','Can add content type'),
 (18,5,'change_contenttype','Can change content type'),
 (19,5,'delete_contenttype','Can delete content type'),
 (20,5,'view_contenttype','Can view content type'),
 (21,6,'add_session','Can add session'),
 (22,6,'change_session','Can change session'),
 (23,6,'delete_session','Can delete session'),
 (24,6,'view_session','Can view session'),
 (25,7,'add_project','Can add project'),
 (26,7,'change_project','Can change project'),
 (27,7,'delete_project','Can delete project'),
 (28,7,'view_project','Can view project'),
 (29,8,'add_avería','Can add avería'),
 (30,8,'change_avería','Can change avería'),
 (31,8,'delete_avería','Can delete avería'),
 (32,8,'view_avería','Can view avería'),
 (33,9,'add_combustible','Can add combustible'),
 (34,9,'change_combustible','Can change combustible'),
 (35,9,'delete_combustible','Can delete combustible'),
 (36,9,'view_combustible','Can view combustible'),
 (37,10,'add_ambulancia','Can add ambulancia'),
 (38,10,'change_ambulancia','Can change ambulancia'),
 (39,10,'delete_ambulancia','Can delete ambulancia'),
 (40,10,'view_ambulancia','Can view ambulancia'),
 (41,11,'add_historialmedico','Can add historial medico'),
 (42,11,'change_historialmedico','Can change historial medico'),
 (43,11,'delete_historialmedico','Can delete historial medico'),
 (44,11,'view_historialmedico','Can view historial medico'),
 (45,12,'add_paciente','Can add paciente'),
 (46,12,'change_paciente','Can change paciente'),
 (47,12,'delete_paciente','Can delete paciente'),
 (48,12,'view_paciente','Can view paciente'),
 (49,13,'add_insumoutilizado','Can add insumo utilizado'),
 (50,13,'change_insumoutilizado','Can change insumo utilizado'),
 (51,13,'delete_insumoutilizado','Can delete insumo utilizado'),
 (52,13,'view_insumoutilizado','Can view insumo utilizado'),
 (53,14,'add_informeemergencia','Can add informe emergencia'),
 (54,14,'change_informeemergencia','Can change informe emergencia'),
 (55,14,'delete_informeemergencia','Can delete informe emergencia'),
 (56,14,'view_informeemergencia','Can view informe emergencia'),
 (57,15,'add_formatoconsentimiento','Can add formato consentimiento'),
 (58,15,'change_formatoconsentimiento','Can change formato consentimiento'),
 (59,15,'delete_formatoconsentimiento','Can delete formato consentimiento'),
 (60,15,'view_formatoconsentimiento','Can view formato consentimiento'),
 (61,16,'add_reporteemergencia','Can add reporte emergencia'),
 (62,16,'change_reporteemergencia','Can change reporte emergencia'),
 (63,16,'delete_reporteemergencia','Can delete reporte emergencia'),
 (64,16,'view_reporteemergencia','Can view reporte emergencia'),
 (65,17,'add_formatorevocacion','Can add formato revocacion'),
 (66,17,'change_formatorevocacion','Can change formato revocacion'),
 (67,17,'delete_formatorevocacion','Can delete formato revocacion'),
 (68,17,'view_formatorevocacion','Can view formato revocacion'),
 (69,18,'add_reportepaciente','Can add reporte paciente'),
 (70,18,'change_reportepaciente','Can change reporte paciente'),
 (71,18,'delete_reportepaciente','Can delete reporte paciente'),
 (72,18,'view_reportepaciente','Can view reporte paciente'),
 (73,19,'add_insumomedico','Can add insumo medico'),
 (74,19,'change_insumomedico','Can change insumo medico'),
 (75,19,'delete_insumomedico','Can delete insumo medico'),
 (76,19,'view_insumomedico','Can view insumo medico'),
 (77,20,'add_checklist','Can add check list'),
 (78,20,'change_checklist','Can change check list'),
 (79,20,'delete_checklist','Can delete check list'),
 (80,20,'view_checklist','Can view check list'),
 (81,21,'add_detallechecklist','Can add detalle check list'),
 (82,21,'change_detallechecklist','Can change detalle check list'),
 (83,21,'delete_detallechecklist','Can delete detalle check list'),
 (84,21,'view_detallechecklist','Can view detalle check list');
INSERT INTO "auth_user" ("id","password","last_login","is_superuser","username","last_name","email","is_staff","is_active","date_joined","first_name") VALUES (1,'pbkdf2_sha256$1000000$t6dRgg9vLvEIfUPE7DnfzC$uvB6o4/m5SGoOJBis3hlan79LafyL06vM/DXFHOiEgM=','2025-06-24 22:24:38.923012',1,'admin','','manustdev@gmail.com',1,1,'2025-06-24 19:46:29.825310','');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (1,'1','ABC-123',1,'[{"added": {}}]',10,1,'2025-06-24 19:51:19.254884'),
 (2,'2','XYZ-345',1,'[{"added": {}}]',10,1,'2025-06-24 19:51:45.483946'),
 (3,'3','FXO-340',1,'[{"added": {}}]',10,1,'2025-06-24 19:52:12.219083'),
 (4,'4','GTH-049',1,'[{"added": {}}]',10,1,'2025-06-24 19:52:43.262914'),
 (5,'5','RHY-493',1,'[{"added": {}}]',10,1,'2025-06-24 19:52:57.339869'),
 (6,'6','RGU-293',1,'[{"added": {}}]',10,1,'2025-06-24 19:53:18.868398'),
 (7,'7','QYH-381',1,'[{"added": {}}]',10,1,'2025-06-24 19:53:43.759383'),
 (8,'1','Avería critico en ABC-123 reportado por Juan Pérez López (2025-06-24)',1,'[{"added": {}}]',8,1,'2025-06-24 21:00:51.366566'),
 (9,'2','Avería leve en XYZ-345 reportado por Carlos Sánchez Castro (2025-06-24)',1,'[{"added": {}}]',8,1,'2025-06-24 21:01:07.733492'),
 (10,'3','Avería grave en FXO-340 reportado por Pedro Ramírez Soto (2025-06-24)',1,'[{"added": {}}]',8,1,'2025-06-24 21:01:26.111285'),
 (11,'4','Avería critico en GTH-049 reportado por Juan Pérez López (2025-06-24)',1,'[{"added": {}}]',8,1,'2025-06-24 21:01:49.338261'),
 (12,'5','Avería leve en RGU-293 reportado por Pedro Ramírez Soto (2025-06-24)',1,'[{"added": {}}]',8,1,'2025-06-24 21:02:18.001995'),
 (13,'6','Avería grave en QYH-381 reportado por Ana Torres Vega (2025-06-24)',1,'[{"added": {}}]',8,1,'2025-06-24 21:02:41.100094'),
 (14,'1','Combustible de ABC-123 registrado por Juan Pérez López el 2025-06-18',1,'[{"added": {}}]',9,1,'2025-06-24 21:08:24.455876'),
 (15,'2','Combustible de QYH-381 registrado por Carlos Sánchez Castro el 2025-06-24',1,'[{"added": {}}]',9,1,'2025-06-24 21:09:05.061491'),
 (16,'3','Combustible de RGU-293 registrado por Pedro Ramírez Soto el 2025-06-15',1,'[{"added": {}}]',9,1,'2025-06-24 21:09:54.482665'),
 (17,'4','Combustible de RGU-293 registrado por Juan Pérez López el 2025-06-01',1,'[{"added": {}}]',9,1,'2025-06-24 21:10:44.483243'),
 (18,'1','Ramirez Soto, Jose - 48765123',1,'[{"added": {}}]',12,1,'2025-06-24 22:36:32.645739'),
 (19,'2','Rojas Morales, Sofía Lucia - 70987654',1,'[{"added": {}}]',12,1,'2025-06-24 22:37:28.846214'),
 (20,'3','Castillo Diaz,, Luis Javier - 45678901',1,'[{"added": {}}]',12,1,'2025-06-24 22:38:31.743498'),
 (21,'4','Flores Espinoza, Laura - 78901234',1,'[{"added": {}}]',12,1,'2025-06-24 22:39:06.390203'),
 (22,'5','Vargas Herrera, Miguel - 41234567',1,'[{"added": {}}]',12,1,'2025-06-24 22:39:38.735522'),
 (23,'6','Soto Vega, Andrea Camila - 76543210',1,'[{"added": {}}]',12,1,'2025-06-24 22:40:28.388799'),
 (24,'7','Ramos Medina, David - 49876543',1,'[{"added": {}}]',12,1,'2025-06-24 22:41:04.414691'),
 (25,'8','Aguilar León, Isabella - 12345678',1,'[{"added": {}}]',12,1,'2025-06-24 22:41:56.993585'),
 (26,'9','Guzmán Delgado, Ricardo Samuel - 87654321',1,'[{"added": {}}]',12,1,'2025-06-24 22:42:50.454213'),
 (27,'2','Historial Médico de Jose - Tipo: O+',1,'[{"added": {}}]',11,1,'2025-06-24 23:04:24.282999'),
 (28,'11',', Manuel - 12345600',3,'',12,1,'2025-06-24 23:04:56.803531'),
 (29,'10',', Mariana - 12345670',3,'',12,1,'2025-06-24 23:05:03.793367'),
 (30,'1','Jr. Ayacucho 3839, Ate - alta - 25/06/2025 02:30',1,'[{"added": {}}]',14,1,'2025-06-25 02:30:54.404716'),
 (31,'2','Jirón Ancash 1415, Cercado de Lima - baja - 25/06/2025 02:31',1,'[{"added": {}}]',14,1,'2025-06-25 02:31:37.911306'),
 (32,'1','CheckList 1 - ABC-123 (2025-06-26)',1,'[{"added": {}}]',20,1,'2025-06-26 02:34:38.859669'),
 (33,'1','InsumoMedico object (1)',1,'[{"added": {}}]',19,1,'2025-06-26 02:35:23.128061'),
 (34,'1','jeringa 20mm - 13',1,'[{"added": {}}]',21,1,'2025-06-26 02:40:44.367909');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry'),
 (2,'auth','permission'),
 (3,'auth','group'),
 (4,'auth','user'),
 (5,'contenttypes','contenttype'),
 (6,'sessions','session'),
 (7,'usuarios','project'),
 (8,'ambulancias','avería'),
 (9,'ambulancias','combustible'),
 (10,'ambulancias','ambulancia'),
 (11,'pacientes','historialmedico'),
 (12,'pacientes','paciente'),
 (13,'emergencias','insumoutilizado'),
 (14,'emergencias','informeemergencia'),
 (15,'emergencias','formatoconsentimiento'),
 (16,'emergencias','reporteemergencia'),
 (17,'emergencias','formatorevocacion'),
 (18,'emergencias','reportepaciente'),
 (19,'inventarios','insumomedico'),
 (20,'inventarios','checklist'),
 (21,'inventarios','detallechecklist');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'contenttypes','0001_initial','2025-06-14 21:04:37.121647'),
 (2,'auth','0001_initial','2025-06-14 21:04:37.142590'),
 (3,'admin','0001_initial','2025-06-14 21:04:37.162354'),
 (4,'admin','0002_logentry_remove_auto_add','2025-06-14 21:04:37.176869'),
 (5,'admin','0003_logentry_add_action_flag_choices','2025-06-14 21:04:37.185877'),
 (6,'contenttypes','0002_remove_content_type_name','2025-06-14 21:04:37.205527'),
 (7,'auth','0002_alter_permission_name_max_length','2025-06-14 21:04:37.220418'),
 (8,'auth','0003_alter_user_email_max_length','2025-06-14 21:04:37.232260'),
 (9,'auth','0004_alter_user_username_opts','2025-06-14 21:04:37.242758'),
 (10,'auth','0005_alter_user_last_login_null','2025-06-14 21:04:37.255232'),
 (11,'auth','0006_require_contenttypes_0002','2025-06-14 21:04:37.260380'),
 (12,'auth','0007_alter_validators_add_error_messages','2025-06-14 21:04:37.270616'),
 (13,'auth','0008_alter_user_username_max_length','2025-06-14 21:04:37.286671'),
 (14,'auth','0009_alter_user_last_name_max_length','2025-06-14 21:04:37.298522'),
 (15,'auth','0010_alter_group_name_max_length','2025-06-14 21:04:37.309542'),
 (16,'auth','0011_update_proxy_permissions','2025-06-14 21:04:37.319817'),
 (17,'auth','0012_alter_user_first_name_max_length','2025-06-14 21:04:37.340518'),
 (18,'sessions','0001_initial','2025-06-14 21:04:37.354823'),
 (19,'usuarios','0001_initial','2025-06-14 21:11:15.527471'),
 (20,'ambulancias','0001_initial','2025-06-24 19:44:56.961557'),
 (21,'pacientes','0001_initial','2025-06-24 22:21:24.730851'),
 (22,'inventarios','0001_initial','2025-06-25 01:12:29.357880'),
 (24,'emergencias','0001_initial','2025-06-26 02:31:47.513627'),
 (25,'inventarios','0002_checklist_detallechecklist','2025-06-26 02:31:47.539200'),
 (26,'inventarios','0003_rename_stock_insumomedico_stockminimo','2025-06-26 02:39:46.379948');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('i7zxl1qdg0ftsdwomw3nhtw49n3mwpe6','.eJxVjEEOwiAURO_C2hBoKR9cuu8ZyIcPUjWQlHZlvLs06UJXk7x5M2_mcN-y21tc3ULsyiS7_DKP4RnLUdADy73yUMu2Lp4fCj_bxudK8XU73b-DjC33dZAmgNJaApK2SlOwKNOUeirQoxkRBgNKiCF1HAV5ZQ2BkjEl6ydkny_USDe-:1uU9cm:-wMeGW8yDWKxCtdI3x-NnfNCnfPkTxkbwVv0geYVBu0','2025-07-08 19:48:08.317939'),
 ('xutuo5eyze9sutzfvrjrqlyf9s5lyqxh','.eJxVjEEOwiAURO_C2hBoKR9cuu8ZyIcPUjWQlHZlvLs06UJXk7x5M2_mcN-y21tc3ULsyiS7_DKP4RnLUdADy73yUMu2Lp4fCj_bxudK8XU73b-DjC33dZAmgNJaApK2SlOwKNOUeirQoxkRBgNKiCF1HAV5ZQ2BkjEl6ydkny_USDe-:1uUC4E:ph0kmG5KEA4eaVwgSaCado0_Rq9u1_o4_gcIaO2I2qE','2025-07-08 22:24:38.929253');
INSERT INTO "inventarios_checklist" ("id","nombre_colaborador","fecha_registro","ambulancia_id") VALUES (1,'Juan Pérez López','2025-06-26 02:34:38.858190',1);
INSERT INTO "inventarios_detallechecklist" ("id","cantidad_contada","checklist_id","insumo_id") VALUES (1,13,1,1);
INSERT INTO "inventarios_insumomedico" ("id","nombre","stock","unidadMedida","tipoAmbulancia") VALUES (1,'jeringa 20mm',10,'unidades','tipo_2');
INSERT INTO "pacientes_historialmedico" ("id","alergias","tipoSangre","enfermedades","paciente_id") VALUES (1,'No presenta alergias','AB+','No presenta enfermedades',12),
 (2,'Alergia al polen','O+','Hipertensión arterial.',1);
INSERT INTO "pacientes_paciente" ("id","nombre","apellido","dni","direccion","email","telefono","fechaNacimiento","sexo") VALUES (1,'Jose','Ramirez Soto','48765123','Av. La Marina 123, Pueblo Libre','jose.ramirez@gmail.com','987654321','1985-03-10','masculino'),
 (2,'Sofía Lucia','Rojas Morales','70987654','Urb. Los Cedros Mz. C Lt. 5, Chorrillos','sofia.rojas@gmail.com','965432109','1998-02-28','femenino'),
 (3,'Luis Javier','Castillo Diaz,','45678901','Jirón Ancash 1415, Cercado de Lima','luis.castillo@gmail.com','943210987','2000-06-23','masculino'),
 (4,'Laura','Flores Espinoza','78901234','Av. Colonial 1617, Callao',NULL,'921098765','2005-06-12','femenino'),
 (5,'Miguel','Vargas Herrera','41234567','Calle Real 1819, Magdalena del Mar',NULL,NULL,'2005-06-28','masculino'),
 (6,'Andrea Camila','Soto Vega','76543210',NULL,'andrea.soto@gmail.com',NULL,'2001-06-13','femenino'),
 (7,'David','Ramos Medina','49876543','Av. La Paz 2223, San Miguel','david.ramos@gmail.com','978901234','2008-06-05','masculino'),
 (8,'Isabella','Aguilar León','12345678','Calle 2 de Mayo 2425, Barranco','isabella.aguilar@email.com','990123456','2004-04-19','femenino'),
 (9,'Ricardo Samuel','Guzmán Delgado','87654321','Av. Faustino Sánchez Carrión 2627, Lince',NULL,'911234567','2006-12-19','masculino'),
 (12,'Manuel','Pérez','72515038','','','','2005-06-28','Masculino');
CREATE INDEX "ambulancias_avería_ambulancia_id_2d6744f9" ON "ambulancias_avería" ("ambulancia_id");
CREATE INDEX "ambulancias_combustible_ambulancia_id_27fbebdc" ON "ambulancias_combustible" ("ambulancia_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "emergencias_informeemergencia_ambulancia_id_a0a52463" ON "emergencias_informeemergencia" ("ambulancia_id");
CREATE INDEX "emergencias_insumoutilizado_insumo_id_0fd3230f" ON "emergencias_insumoutilizado" ("insumo_id");
CREATE INDEX "emergencias_insumoutilizado_reporte_id_b78674e4" ON "emergencias_insumoutilizado" ("reporte_id");
CREATE INDEX "emergencias_reportepaciente_paciente_id_801ef025" ON "emergencias_reportepaciente" ("paciente_id");
CREATE INDEX "emergencias_reportepaciente_reporte_id_9ed87855" ON "emergencias_reportepaciente" ("reporte_id");
CREATE INDEX "inventarios_checklist_ambulancia_id_b922ae8c" ON "inventarios_checklist" ("ambulancia_id");
CREATE INDEX "inventarios_detallechecklist_checklist_id_2b582162" ON "inventarios_detallechecklist" ("checklist_id");
CREATE INDEX "inventarios_detallechecklist_insumo_id_c35737b4" ON "inventarios_detallechecklist" ("insumo_id");
COMMIT;
