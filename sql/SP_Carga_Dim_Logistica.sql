USE sublimatech
GO

CREATE PROCEDURE SP_Carga_Logistica
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        MERGE INTO logistica AS target
        USING (
            SELECT DISTINCT TRIM(empresa_logistica) AS nombre_empresa
            FROM stg_logistics
            WHERE empresa_logistica IS NOT NULL
        ) AS Source
        ON target.nombre_empresa = Source.nombre_empresa
        
        WHEN MATCHED THEN
            UPDATE SET target.nombre_empresa = Source.nombre_empresa
            
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (nombre_empresa)
            VALUES (Source.nombre_empresa);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO