'use strict';
const electron = require('electron');
const app = electron.app; // Module to control application life.
const BrowserWindow = electron.BrowserWindow; // Module to create native browser window.

const connect = require('connect');
const serveStatic = require('serve-static');

var util = require('util'),
  spawn = require('child_process').spawn,
  // the second arg is the command options
  csiproc = spawn(__dirname + '/electron-run.sh', ['2', __dirname + '/../dat/electron.dat']);

csiproc.stdout.on('data', function(data) { // register one or more handlers
  console.log('stdout: ' + data);
  if (data.toString().lastIndexOf('REFRESH', 0) === 0) {
    mainWindow.loadURL(`file://${__dirname}/img/plot.png`);
  }
});

csiproc.stderr.on('data', function(data) {
  console.log('stderr: ' + data);
});

csiproc.on('exit', function(code) {
  console.log('child process exited with code ' + code);
});

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

// Quit when all windows are closed.
app.on('window-all-closed', function() {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform != 'darwin') {
    app.quit();
  }
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.on('ready', function() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 768,
    height: 576
  });

  // and load the index.html of the app.
  mainWindow.loadURL(`file://${__dirname}/index.html`);

  // serve plots on LAN
  connect().use(serveStatic(`${__dirname}/img`)).listen(8080);

  // Emitted when the window is closed.
  mainWindow.on('closed', function() {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
    // send SIGTERM to process
    csiproc.kill();
  });
});
