USE sublimatech
GO

CREATE TABLE maquinaria (
	sk_maquina INT IDENTITY(1,1) NOT NULL,
	id_maquina VARCHAR(255) NOT NULL,
	CONSTRAINT PK_Dim_Maquinaria PRIMARY KEY(sk_maquina)
);
GO

CREATE TABLE operador(
	sk_operador INT IDENTITY(1,1) NOT NULL,
	nombre_operador VARCHAR(255) NOT NULL,
	CONSTRAINT PK_Dim_operador PRIMARY KEY(sk_operador)
);
GO

CREATE TABLE logistica (
    sk_empresa INT IDENTITY(1,1) NOT NULL,
    nombre_empresa VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Dim_Logistica PRIMARY KEY(sk_empresa)
);
GO

CREATE TABLE producto (
    sk_producto INT IDENTITY(1,1) NOT NULL,
    nombre_producto VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Dim_Producto PRIMARY KEY(sk_producto)
);
GO

CREATE TABLE geografia (
    sk_ubicacion INT IDENTITY(1,1) NOT NULL,
    region VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Dim_Geografia PRIMARY KEY(sk_ubicacion)
);
GO

CREATE TABLE fecha (
    fecha DATE NOT NULL,
    dia TINYINT NOT NULL,
    mes TINYINT NOT NULL,
    anio SMALLINT NOT NULL,
    nombre_dia VARCHAR(50) NOT NULL,
    nombre_mes VARCHAR(50) NOT NULL,
    semestre TINYINT NOT NULL,
    trimestre TINYINT NOT NULL,
    CONSTRAINT PK_Dim_Fecha PRIMARY KEY(fecha)
);
GO

-- ==========================================
-- TABLA DE HECHOS (FACT TABLE)
-- ==========================================

CREATE TABLE fact_ventas (
    sk_venta INT IDENTITY(1,1) NOT NULL,
    
    -- Dimensiones Degeneradas
    orden VARCHAR(255),
    tracking_id VARCHAR(255),

    -- Claves Foráneas (Dimensiones base)
    sk_maquina INT,
    sk_operador INT,
    sk_empresa INT,
    sk_ubicacion INT,
    sk_producto INT,

    -- Claves Foráneas (Dimensiones de Rol: Fechas)
    fecha DATE,
    sk_fecha_inicio_estampado DATE,
    sk_fecha_fin_confeccion DATE,
    sk_fecha_despacho DATE,
    sk_fecha_entrega DATE,

    -- Horarios (TIME crudo)
    hora_compra TIME,
    hora_inicio_estampado TIME,
    hora_fin_confeccion TIME,
    hora_despacho TIME,
    hora_entrega TIME,

    -- Métricas y Banderas
    control_calidad BIT,
    cantidad SMALLINT,
    ingreso_total DECIMAL(12,2),
    precio_unitario DECIMAL(12,2),
    costo_envio DECIMAL(12,2),

    CONSTRAINT PK_Fact_Ventas PRIMARY KEY(sk_venta),

    -- Referencias (Foreign Keys)
    CONSTRAINT FK_Fact_Maquina FOREIGN KEY (sk_maquina) REFERENCES maquinaria(sk_maquina),
    CONSTRAINT FK_Fact_Operador FOREIGN KEY (sk_operador) REFERENCES operador(sk_operador),
    CONSTRAINT FK_Fact_Empresa FOREIGN KEY (sk_empresa) REFERENCES logistica(sk_empresa),
    CONSTRAINT FK_Fact_Ubicacion FOREIGN KEY (sk_ubicacion) REFERENCES geografia(sk_ubicacion),
    CONSTRAINT FK_Fact_Producto FOREIGN KEY (sk_producto) REFERENCES producto(sk_producto),

    -- Referencias de Fecha
    CONSTRAINT FK_Fact_FechaCompra FOREIGN KEY (fecha) REFERENCES fecha(fecha),
    CONSTRAINT FK_Fact_FechaEstampado FOREIGN KEY (sk_fecha_inicio_estampado) REFERENCES fecha(fecha),
    CONSTRAINT FK_Fact_FechaConfeccion FOREIGN KEY (sk_fecha_fin_confeccion) REFERENCES fecha(fecha),
    CONSTRAINT FK_Fact_FechaDespacho FOREIGN KEY (sk_fecha_despacho) REFERENCES fecha(fecha),
    CONSTRAINT FK_Fact_FechaEntrega FOREIGN KEY (sk_fecha_entrega) REFERENCES fecha(fecha)
);
GO