-- Tabla de roles
CREATE TABLE roles (
    role_name VARCHAR(10) PRIMARY KEY CHECK (role_name IN ('USER', 'EMPLOYEE'))
);

-- Tabla de idiomas
CREATE TABLE languages (
    language_code VARCHAR(5) PRIMARY KEY CHECK (language_code IN ('es-ES', 'en-US'))
);

-- Tabla de dispositivos de acceso
CREATE TABLE access_devices (
    device_type VARCHAR(10) PRIMARY KEY CHECK (device_type IN ('WEB', 'MOBILE'))
);

-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    nick_name VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(10) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    image VARCHAR(255),
    is_blocked BOOLEAN DEFAULT FALSE,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role) REFERENCES roles(role_name)
);

-- Tabla de productos
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image VARCHAR(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de regiones de productos
CREATE TABLE product_regions (
    product_id UUID,
    region_code VARCHAR(10),
    PRIMARY KEY (product_id, region_code),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Tabla de contenido de productos por idioma
CREATE TABLE product_lan_contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID,
    lan VARCHAR(5),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (lan) REFERENCES languages(language_code)
);

-- Tabla de blogs
CREATE TABLE blogs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID,
    image VARCHAR(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Tabla de contenido de blogs por idioma
CREATE TABLE blog_lan_contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID,
    lan VARCHAR(5),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (blog_id) REFERENCES blogs(id) ON DELETE CASCADE,
    FOREIGN KEY (lan) REFERENCES languages(language_code)
);

-- Tabla de comentarios de blogs
CREATE TABLE blog_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID,
    user_id UUID,
    comment TEXT NOT NULL,
    image VARCHAR(255),
    n_likes INTEGER DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (blog_id) REFERENCES blogs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla de solicitudes de productos
CREATE TABLE product_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    user_id UUID,
    image VARCHAR(255),
    description TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla de solicitudes de blogs
CREATE TABLE blog_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    product_id UUID,
    image VARCHAR(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Tabla de comentarios en solicitudes de blogs
CREATE TABLE blog_request_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_request_id UUID,
    user_id UUID,
    comment TEXT NOT NULL,
    image VARCHAR(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (blog_request_id) REFERENCES blog_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla de accesos a recursos
CREATE TABLE resource_accesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    resource_type VARCHAR(255) NOT NULL,
    resource_id UUID NOT NULL,
    access_type VARCHAR(255) NOT NULL,
    access_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_type VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (device_type) REFERENCES access_devices(device_type)
);

-- Tabla de foros
CREATE TABLE forums (
    region_id VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL
);

-- Tabla de hilos
CREATE TABLE threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id VARCHAR(10),
    lan VARCHAR(5),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES forums(region_id) ON DELETE CASCADE,
    FOREIGN KEY (lan) REFERENCES languages(language_code)
);

-- Tabla de comentarios en hilos
CREATE TABLE thread_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID,
    user_id UUID,
    content TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Insertar datos iniciales
INSERT INTO roles (role_name) VALUES ('USER'), ('EMPLOYEE');
INSERT INTO languages (language_code) VALUES ('es-ES'), ('en-US');
INSERT INTO access_devices (device_type) VALUES ('WEB'), ('MOBILE');

-- Insertar usuario admin
INSERT INTO users (
    email,
    nick_name,
    role,
    hashed_password,
    image,
    is_blocked,
    creation_date
) VALUES (
    'admin@example.com',
    'admin',
    'EMPLOYEE',
    '$2b$12$orpklA3o8MWZ2CVzIdYMjeqa1EoZuN.zr4dh7lmWQqqbx5WEfVtZ6', -- password: admin123
    'https://randomuser.me/api/portraits/men/1.jpg',
    false,
    CURRENT_TIMESTAMP
);


-- Ahora sí podemos insertar los productos
INSERT INTO products (id, image, creation_date)
VALUES (
    '11111111-1111-1111-1111-111111111111', -- Reemplazar con el UUID real
    'https://bucket.lucantel.es/consume-images/aceite-oliva.png',
    CURRENT_TIMESTAMP - INTERVAL '15 days'
);

-- Insertar las regiones del primer producto
INSERT INTO product_regions (product_id, region_code)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'ES-AN'),
    ('11111111-1111-1111-1111-111111111111', 'ES-CM');

-- Insertar los contenidos del primer producto
INSERT INTO product_lan_contents (id, product_id, lan, name, description)
VALUES 
    (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'es-ES', 'Aceite de oliva virgen', 'Aceite de oliva virgen extra de la mejor calidad'),
    (gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 'en-US', 'Virgin olive oil', 'Extra virgin olive oil of the highest quality');

-- Insertar el segundo producto (Jamón ibérico)
INSERT INTO products (id, image, creation_date)
VALUES (
    '22222222-2222-2222-2222-222222222222', -- Reemplazar con el UUID real
    'https://bucket.lucantel.es/consume-images/jamon-iberico.jpg',
    CURRENT_TIMESTAMP - INTERVAL '10 days'
);

-- Insertar las regiones del segundo producto
INSERT INTO product_regions (product_id, region_code)
VALUES 
    ('22222222-2222-2222-2222-222222222222', 'ES-EX'),
    ('22222222-2222-2222-2222-222222222222', 'ES-AN');

-- Insertar los contenidos del segundo producto
INSERT INTO product_lan_contents (id, product_id, lan, name, description)
VALUES 
    (gen_random_uuid(), '22222222-2222-2222-2222-222222222222', 'es-ES', 'Jamón ibérico', 'Jamón ibérico de bellota');