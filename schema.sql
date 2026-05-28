-- ========================================
-- SQL СХЕМА БАЗЫ ДАННЫХ "РукоДел"
-- Совместимость: MySQL 8.0+, MariaDB 10.5+
-- ========================================

-- Создание базы данных
CREATE DATABASE IF NOT EXISTS rukodel 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE rukodel;

-- ========================================
-- ТАБЛИЦА: users (Пользователи)
-- ========================================
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150) DEFAULT '',
    last_name VARCHAR(150) DEFAULT '',
    role ENUM('buyer', 'master', 'admin') DEFAULT 'buyer',
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: masters (Мастера)
-- ========================================
CREATE TABLE IF NOT EXISTS masters (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    description TEXT,
    avatar VARCHAR(255),
    rating DECIMAL(3, 2) DEFAULT 0.00 CHECK (rating >= 0.00 AND rating <= 5.00),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_specialty (specialty),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: categories (Категории)
-- ========================================
CREATE TABLE IF NOT EXISTS categories (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    
    INDEX idx_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: products (Товары)
-- ========================================
CREATE TABLE IF NOT EXISTS products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    master_id BIGINT NOT NULL,
    category_id BIGINT,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    quantity INT UNSIGNED DEFAULT 0,
    image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (master_id) REFERENCES masters(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_category_active (category_id, is_active),
    INDEX idx_master_active (master_id, is_active),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: orders (Заказы)
-- ========================================
CREATE TABLE IF NOT EXISTS orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    delivery_address TEXT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: order_items (Позиции заказа)
-- ========================================
CREATE TABLE IF NOT EXISTS order_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT UNSIGNED NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: cart (Корзина)
-- ========================================
CREATE TABLE IF NOT EXISTS cart (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT UNSIGNED DEFAULT 1 CHECK (quantity > 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТАБЛИЦА: reviews (Отзывы)
-- ========================================
CREATE TABLE IF NOT EXISTS reviews (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    rating SMALLINT UNSIGNED NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_product_user (product_id, user_id),
    INDEX idx_product (product_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================================
-- ТЕСТОВЫЕ ДАННЫЕ
-- ========================================

-- Добавление тестовых категорий
INSERT INTO categories (name, slug, description) VALUES
    ('Керамика', 'keramika', 'Изделия из керамики: вазы, посуда, декор'),
    ('Текстиль', 'textil', 'Текстильные изделия: вышивка, подушки, скатерти'),
    ('Украшения', 'ukrasheniya', 'Авторские украшения из серебра и камней'),
    ('Изделия из дерева', 'derevo', 'Деревянные изделия: шкатулки, посуда, декор');

-- Добавление тестового пользователя-администратора
-- Пароль: admin123 (в реальном проекте используйте хэш!)
INSERT INTO users (username, email, password, first_name, last_name, role, is_staff, is_superuser) VALUES
    ('admin', 'admin@rukodel.ru', 'pbkdf2_sha256$600000$...', 'Администратор', 'Системы', 'admin', TRUE, TRUE);

-- Примечание: пароли должны быть захэшированы через Django!
-- Для создания суперпользователя используйте команду:
-- python manage.py createsuperuser

-- ========================================
-- ПРЕДСТАВЛЕНИЯ (VIEWS) ДЛЯ АНАЛИТИКИ
-- ========================================

-- Представление: Популярные товары
CREATE OR REPLACE VIEW popular_products AS
SELECT 
    p.id,
    p.name,
    p.price,
    p.quantity,
    m.specialty AS master_specialty,
    CONCAT(u.first_name, ' ', u.last_name) AS master_name,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.quantity) AS total_sold,
    AVG(r.rating) AS avg_rating
FROM products p
LEFT JOIN masters m ON p.master_id = m.id
LEFT JOIN users u ON m.user_id = u.id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN reviews r ON p.id = r.product_id
WHERE p.is_active = TRUE
GROUP BY p.id
ORDER BY total_sold DESC, avg_rating DESC;

-- Представление: Статистика по мастерам
CREATE OR REPLACE VIEW masters_stats AS
SELECT 
    m.id,
    CONCAT(u.first_name, ' ', u.last_name) AS master_name,
    m.specialty,
    m.rating,
    COUNT(DISTINCT p.id) AS products_count,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    COALESCE(SUM(oi.quantity * oi.price), 0) AS total_revenue
FROM masters m
LEFT JOIN users u ON m.user_id = u.id
LEFT JOIN products p ON m.id = p.master_id
LEFT JOIN order_items oi ON p.id = oi.product_id
GROUP BY m.id
ORDER BY total_revenue DESC;

-- ========================================
-- ХРАНИМЫЕ ПРОЦЕДУРЫ
-- ========================================

DELIMITER $$

-- Процедура: Обновление рейтинга мастера
CREATE PROCEDURE update_master_rating(IN master_id_param BIGINT)
BEGIN
    DECLARE avg_rating DECIMAL(3, 2);
    
    SELECT COALESCE(AVG(r.rating), 0)
    INTO avg_rating
    FROM reviews r
    JOIN products p ON r.product_id = p.id
    WHERE p.master_id = master_id_param;
    
    UPDATE masters
    SET rating = avg_rating
    WHERE id = master_id_param;
END$$

-- Процедура: Получение товаров в наличии по категории
CREATE PROCEDURE get_products_by_category(IN category_slug_param VARCHAR(100))
BEGIN
    SELECT 
        p.id,
        p.name,
        p.description,
        p.price,
        p.quantity,
        p.image,
        c.name AS category_name,
        CONCAT(u.first_name, ' ', u.last_name) AS master_name
    FROM products p
    JOIN categories c ON p.category_id = c.id
    JOIN masters m ON p.master_id = m.id
    JOIN users u ON m.user_id = u.id
    WHERE c.slug = category_slug_param
        AND p.is_active = TRUE
        AND p.quantity > 0
    ORDER BY p.created_at DESC;
END$$

DELIMITER ;

-- ========================================
-- ТРИГГЕРЫ
-- ========================================

DELIMITER $$

-- Триггер: Обновление рейтинга мастера при добавлении отзыва
CREATE TRIGGER after_review_insert
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
    DECLARE master_id_var BIGINT;
    
    SELECT master_id INTO master_id_var
    FROM products
    WHERE id = NEW.product_id;
    
    CALL update_master_rating(master_id_var);
END$$

-- Триггер: Обновление рейтинга мастера при изменении отзыва
CREATE TRIGGER after_review_update
AFTER UPDATE ON reviews
FOR EACH ROW
BEGIN
    DECLARE master_id_var BIGINT;
    
    SELECT master_id INTO master_id_var
    FROM products
    WHERE id = NEW.product_id;
    
    CALL update_master_rating(master_id_var);
END$$

DELIMITER ;

-- ========================================
-- ПРИМЕРЫ ЗАПРОСОВ
-- ========================================

-- Получить все товары с информацией о мастере
SELECT 
    p.id,
    p.name,
    p.price,
    p.quantity,
    c.name AS category,
    CONCAT(u.first_name, ' ', u.last_name) AS master_name,
    m.specialty
FROM products p
JOIN categories c ON p.category_id = c.id
JOIN masters m ON p.master_id = m.id
JOIN users u ON m.user_id = u.id
WHERE p.is_active = TRUE
ORDER BY p.created_at DESC;

-- Получить заказы пользователя
SELECT 
    o.id,
    o.total_price,
    o.status,
    o.created_at,
    COUNT(oi.id) AS items_count
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = 1
GROUP BY o.id
ORDER BY o.created_at DESC;

-- Получить содержимое корзины с подсчётом суммы
SELECT 
    c.id,
    p.name,
    p.price,
    c.quantity,
    (p.price * c.quantity) AS subtotal
FROM cart c
JOIN products p ON c.product_id = p.id
WHERE c.user_id = 1;
