USE sublimatech
GO

CREATE PROCEDURE SP_Carga_Maquinaria
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        MERGE INTO maquinaria AS target
        USING (
            -- Filtrar nulos para evitar que se cree una máquina en blanco
            SELECT DISTINCT TRIM(sp.id_maquina) AS id_maquina
            FROM stg_production sp
            WHERE sp.id_maquina IS NOT NULL
        ) AS Source
        ON target.id_maquina = Source.id_maquina
        
        WHEN MATCHED THEN
            UPDATE SET target.id_maquina = Source.id_maquina
            
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (id_maquina)
            VALUES (Source.id_maquina);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO