USE sublimatech
GO

CREATE PROCEDURE SP_Carga_Producto
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        MERGE INTO producto AS target
        USING (
            SELECT DISTINCT TRIM(articulo) AS nombre_producto
            FROM stg_sales
            WHERE articulo IS NOT NULL
        ) AS Source
        ON target.nombre_producto = Source.nombre_producto
        
        WHEN MATCHED THEN
            UPDATE SET target.nombre_producto = Source.nombre_producto
            
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (nombre_producto)
            VALUES (Source.nombre_producto);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO