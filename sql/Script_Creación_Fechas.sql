USE sublimatech;
GO

-- Configurar el idioma para que:
-- Lunes = día 1
-- Sábado = día 6
-- Domingo = día 7
SET LANGUAGE Spanish;
GO

DECLARE @FechaInicio DATE = '2025-01-01';
DECLARE @FechaFin    DATE = '2030-12-31';

WHILE @FechaInicio <= @FechaFin
BEGIN

    -- Solo inserta si la fecha no existe previamente
    IF NOT EXISTS (
        SELECT 1 
        FROM dbo.fecha 
        WHERE fecha = @FechaInicio
    )
    BEGIN

        INSERT INTO dbo.fecha (
            fecha,
            dia,
            mes,
            anio,
            nombre_mes,
            nombre_dia,
            semestre,
            trimestre
        )
        VALUES (
            @FechaInicio,                                      -- fecha
            DAY(@FechaInicio),                                 -- día
            MONTH(@FechaInicio),                               -- mes
            YEAR(@FechaInicio),                                -- año

            -- Nombre del mes
            UPPER(LEFT(DATENAME(MONTH, @FechaInicio), 1)) + 
            LOWER(SUBSTRING(DATENAME(MONTH, @FechaInicio), 2, 50)),

            -- Nombre del día
            UPPER(LEFT(DATENAME(WEEKDAY, @FechaInicio), 1)) + 
            LOWER(SUBSTRING(DATENAME(WEEKDAY, @FechaInicio), 2, 50)),

            -- Semestre
            CASE 
                WHEN MONTH(@FechaInicio) <= 6 THEN 1
                ELSE 2
            END,

            -- Trimestre
            DATEPART(QUARTER, @FechaInicio)
        );

    END;

    -- Pasar al siguiente día
    SET @FechaInicio = DATEADD(DAY, 1, @FechaInicio);

END;
GO