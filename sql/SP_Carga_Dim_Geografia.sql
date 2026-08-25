USE sublimatech;
GO

CREATE PROCEDURE SP_Carga_Geografia
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON; -- Si algo falla, interrumpe y prepara el rollback automático

    BEGIN TRY
        BEGIN TRANSACTION;

        -- 1. Validaciones previas
        IF EXISTS (SELECT 1 FROM stg_logistics sl WHERE sl.provincia_destino IS NULL)
        BEGIN
            THROW 51000, 'Hay destinos en stg nulos, abortando carga.', 1;
        END

        -- 2. MERGE (upsert) para asegurar idempotencia
        MERGE INTO geografia AS target
        USING (
            SELECT DISTINCT TRIM(sl.provincia_destino) AS region
            FROM stg_logistics sl
        ) AS Source
        ON target.region = Source.region
        
        WHEN MATCHED THEN
            UPDATE SET target.region = Source.region
            
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (region)
            VALUES (Source.region);

        -- 3. Confirmamos la transacción si todo fue exitoso
        COMMIT TRANSACTION;
    END TRY
    
    BEGIN CATCH
        -- 4. Manejo de errores y Rollback
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        -- Re-lanzamos el error a la consola para saber qué falló
        THROW;
    END CATCH
END;
GO