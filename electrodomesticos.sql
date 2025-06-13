
CREATE TABLE IF NOT EXISTS electrodomesticos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    potencia_w REAL,
    uso_diario_h REAL,
    consumo_diario_wh REAL,
    consumo_mensual_kwh REAL
);

INSERT INTO electrodomesticos (nombre, categoria, potencia_w, uso_diario_h, consumo_diario_wh, consumo_mensual_kwh) VALUES
('Bombilla LED', 'Iluminación', 10, 5, 50, 1.5),
('Bombilla incandescente', 'Iluminación', 60, 5, 300, 9),
('Frigorífico (A++)', 'Electrodomésticos', 150, 24, 3600, 108),
('Televisor LED (32")', 'Electrodomésticos', 60, 4, 240, 7.2),
('Ordenador portátil', 'Informática', 50, 5, 250, 7.5),
('Ordenador de sobremesa', 'Informática', 250, 5, 1250, 37.5),
('Microondas', 'Cocina', 1000, 0.5, 500, 15),
('Lavadora', 'Electrodomésticos', 1500, 0.5, 750, 11.25),
('Lavavajillas', 'Electrodomésticos', 1800, 0.5, 900, 13.5),
('Aire acondicionado (frío)', 'Climatización', 2000, 4, 8000, 240),
('Estufa eléctrica', 'Climatización', 2000, 3, 6000, 180),
('Consola de videojuegos', 'Ocio', 120, 2, 240, 7.2),
('Cargador de móvil', 'Cargadores', 5, 2, 10, 0.3),
('Router Wi-Fi', 'Redes', 10, 24, 240, 7.2),
('Secador de pelo', 'Higiene', 1800, 0.2, 360, 10.8),
('Horno eléctrico', 'Cocina', 2000, 1, 2000, 60),
('Plancha', 'Hogar', 1200, 0.5, 600, 18),
('Cafetera eléctrica', 'Cocina', 1000, 0.3, 300, 9),
('Aspiradora', 'Limpieza', 1400, 0.3, 420, 12.6),
('Impresora', 'Informática', 30, 1, 30, 0.9),
('Monitor de PC (24")', 'Informática', 30, 5, 150, 4.5);
