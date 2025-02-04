const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { promisify } = require('util');

const renameAsync = promisify(fs.rename);

let mainWindow;

// Función para renombrar archivos
async function renameFiles(archivosSeleccionados, nombrePersonalizado, identificador, numeroInicial) {
  try {
    for (const archivoSeleccionado of archivosSeleccionados) {
      const directorio = path.dirname(archivoSeleccionado);
      const extension = path.extname(archivoSeleccionado);
      const nombreNuevo = `${nombrePersonalizado}${identificador}${numeroInicial}${extension}`;
      const rutaNueva = path.join(directorio, nombreNuevo);

      // Renombrar el archivo
      await renameAsync(archivoSeleccionado, rutaNueva);
      numeroInicial += 1; // Incrementar el número correlativo
    }

    return { success: true, message: 'Archivos renombrados correctamente.' };
  } catch (error) {
    return { success: false, message: `Error al renombrar los archivos: ${error.message}` };
  }
}

// Crear la ventana principal
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 600,
    height: 400,
    icon: path.join(__dirname,'icon.ico'),
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    resizable: false,
    maximizable: false,
    fullscreenable: false,
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Manejar la selección de archivos
  ipcMain.handle('select-files', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openFile', 'multiSelections'],
    });
    return result.filePaths;
  });

  // Manejar el renombrado de archivos
  ipcMain.handle('rename-files', async (event, { archivos, nombrePersonalizado, identificador, numeroInicial }) => {
    return renameFiles(archivos, nombrePersonalizado, identificador, numeroInicial);
  });

  // Manejar cuadros de diálogo de error
  ipcMain.handle('show-error-dialog', async (event, { title, message }) => {
    await dialog.showErrorBox(title, message);
  });

  // Manejar cuadros de diálogo de información
  ipcMain.handle('show-info-dialog', async (event, { title, message }) => {
    await dialog.showMessageBox({
      type: 'info',
      title,
      message,
    });
  });
}

// Iniciar la aplicación
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});