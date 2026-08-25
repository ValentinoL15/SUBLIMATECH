USE sublimatech
GO

USE sublimatech;
GO

CREATE PROCEDURE SP_Carga_Fact_Ventas
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        MERGE INTO fact_ventas AS target
        USING (
            SELECT 
                -- 1. Dimensiones Degeneradas
                v.id_pedido AS orden,
                l.tracking_id,

                -- 2. Búsqueda de Surrogate Keys (sk_) en las Dimensiones
                m.sk_maquina,
                o.sk_operador,
                emp.sk_empresa,
                g.sk_ubicacion,
                p.sk_producto,

                -- 3. Búsqueda de Fechas (Role-Playing Dimensions a YYYYMMDD)
                -- Convertimos el datetime a un entero formato YYYYMMDD (Ej: 20260515)
                CAST(v.fecha_de_compra AS DATE) AS sk_fecha_compra,
                CAST(pr.fecha_inicio_estampado AS DATE) AS sk_fecha_inicio_estampado,
                CAST(pr.fecha_fin_confeccion AS DATE) AS sk_fecha_fin_confeccion,
                CAST(l.fecha_despacho AS DATE) sk_fecha_despacho,
                CAST(l.fecha_entrega AS DATE) AS sk_fecha_entrega,

                -- 4. Extracción de Horarios puros (TIME)
                CAST(v.horario AS TIME) AS hora_compra,
                CAST(pr.hora_inicio_estampado AS TIME) AS hora_inicio_estampado,
                CAST(pr.hora_fin_confeccion AS TIME) AS hora_fin_confeccion,
                CAST(l.hora_despacho AS TIME) AS hora_despacho,
                CAST(l.hora_entrega AS TIME) AS hora_entrega,

                -- 5. Métricas y Banderas
                pr.control_calidad AS control_calidad,
                v.cantidad,
                v.ingreso_total,
                -- Calculamos el precio unitario al vuelo protegiendo contra división por cero
                CAST((v.ingreso_total / NULLIF(v.cantidad, 0)) AS DECIMAL(12,2)) AS precio_unitario,
                l.costo_envio

            FROM stg_sales v
            -- Unimos las tres tablas de origen limpio usando el ID del pedido
            LEFT JOIN stg_production pr ON v.id_pedido = pr.pedido_ref
            LEFT JOIN stg_logistics l ON v.id_pedido = l.orden
            
            -- Unimos las dimensiones para traducir los textos en IDs enteros (sk)
            LEFT JOIN producto p ON TRIM(v.articulo) = p.nombre_producto
            LEFT JOIN maquinaria m ON TRIM(pr.id_maquina) = m.id_maquina
            LEFT JOIN operador o ON COALESCE(TRIM(pr.operador), 'Sin Asignar') = o.nombre_operador
            LEFT JOIN logistica emp ON TRIM(l.empresa_logistica) = emp.nombre_empresa
            LEFT JOIN geografia g ON TRIM(l.provincia_destino) = g.region
        ) AS Source
        ON target.orden = Source.orden
        
        -- Si la orden ya existe, actualizamos todos los campos por si hubo cambios en logística o producción
        WHEN MATCHED THEN
            UPDATE SET 
                target.tracking_id = Source.tracking_id,
                target.sk_maquina = Source.sk_maquina,
                target.sk_operador = Source.sk_operador,
                target.sk_empresa = Source.sk_empresa,
                target.sk_ubicacion = Source.sk_ubicacion,
                target.sk_producto = Source.sk_producto,
                target.fecha = Source.sk_fecha_compra,
                target.sk_fecha_inicio_estampado = Source.sk_fecha_inicio_estampado,
                target.sk_fecha_fin_confeccion = Source.sk_fecha_fin_confeccion,
                target.sk_fecha_despacho = Source.sk_fecha_despacho,
                target.sk_fecha_entrega = Source.sk_fecha_entrega,
                target.hora_compra = Source.hora_compra,
                target.hora_inicio_estampado = Source.hora_inicio_estampado,
                target.hora_fin_confeccion = Source.hora_fin_confeccion,
                target.hora_despacho = Source.hora_despacho,
                target.hora_entrega = Source.hora_entrega,
                target.control_calidad = Source.control_calidad,
                target.cantidad = Source.cantidad,
                target.ingreso_total = Source.ingreso_total,
                target.precio_unitario = Source.precio_unitario,
                target.costo_envio = Source.costo_envio

        -- Si la orden es nueva, insertamos el registro completo
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (
                orden, tracking_id, 
                sk_maquina, sk_operador, sk_empresa, sk_ubicacion, sk_producto,
                fecha, sk_fecha_inicio_estampado, sk_fecha_fin_confeccion, sk_fecha_despacho, sk_fecha_entrega,
                hora_compra, hora_inicio_estampado, hora_fin_confeccion, hora_despacho, hora_entrega,
                control_calidad, cantidad, ingreso_total, precio_unitario, costo_envio
            )
            VALUES (
                Source.orden, Source.tracking_id,
                Source.sk_maquina, Source.sk_operador, Source.sk_empresa, Source.sk_ubicacion, Source.sk_producto,
                Source.sk_fecha_compra, Source.sk_fecha_inicio_estampado, Source.sk_fecha_fin_confeccion, Source.sk_fecha_despacho, Source.sk_fecha_entrega,
                Source.hora_compra, Source.hora_inicio_estampado, Source.hora_fin_confeccion, Source.hora_despacho, Source.hora_entrega,
                Source.control_calidad, Source.cantidad, Source.ingreso_total, Source.precio_unitario, Source.costo_envio
            );

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO