USE sublimatech
GO

CREATE PROCEDURE SP_Carga_Operador
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        MERGE INTO operador AS target
        USING (
            -- Reemplazamos los nulos por 'Sin Asignar' para no romper referencialidad
            SELECT DISTINCT COALESCE(TRIM(operador), 'Sin Asignar') AS nombre_operador
            FROM stg_production
        ) AS Source
        ON target.nombre_operador = Source.nombre_operador
        
        WHEN MATCHED THEN
            UPDATE SET target.nombre_operador = Source.nombre_operador
            
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (nombre_operador)
            VALUES (Source.nombre_operador);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO