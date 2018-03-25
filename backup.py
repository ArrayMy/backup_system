#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, shutil, json, time, io


def main(workspaceFolder, backUpspaceFolder):
    childFolder = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()));
    backUpspaceFolder = os.path.join(backUpspaceFolder, childFolder);

    if os.path.exists(backUpspaceFolder) == False:
        os.makedirs(backUpspaceFolder)
    else:
        print backUpspaceFolder + ' has existed!'
        sys.exit()

    print 'sourcepath:' + workspaceFolder;
    print 'backpath:' + backUpspaceFolder;

    traverseAllFile(workspaceFolder, backUpspaceFolder, workspaceFolder)


def traverseAllFile(sourcePath, backUpspaceFolder, originalPath):
    if sourcePath.startswith(backUpspaceFolderflag):
        return;
    for i in os.listdir(sourcePath):
        if i in Ignore:
            continue;
        filepath = os.path.join(sourcePath, i);
        if isDestFile(filepath):

            childFilePath = filepath.split(originalPath);
            if len(childFilePath) != 2:
                print 'dosomething is wrong in childFilePath:' + childFilePath;
                sys.exit();
            childFileName = getPathWithoutSeparate(childFilePath[1]);
            backUpFilePath = os.path.join(backUpspaceFolder, childFileName);
            backDirpath = os.path.dirname(backUpFilePath);
            if os.path.exists(backDirpath) == False:
                os.makedirs(backDirpath)

            shutil.copy(filepath, backUpFilePath);
            print 'backup file:' + filepath + ' to ' + backUpFilePath;

        if os.path.isdir(filepath):
            traverseAllFile(filepath, backUpspaceFolder, originalPath, remoteePath)


def getPathWithoutSeparate(path):
    newpath = '';
    trans = False;
    for i in path:
        if i == os.path.sep and trans == False:
            continue
        else:
            trans = True;
            newpath += i;
    return newpath;


def isDestFile(path):
    return path.endswith(Type) and os.path.isfile(path);


if __name__ == '__main__':
    global Type;
    global backUpspaceFolderflag;
    global Ignore;
    global config;
    num = 0;
    configFile = None;
    timeStep = 3600;
    Loop = 0;
    try:
        configFile = io.open(os.path.join(os.getcwd(), 'backup.config'), mode="r", encoding="utf-8");
        content = configFile.read();
        config = json.loads(content.replace('\r\n', '\\r\\n'), encoding="utf-8");

        WorkspaceFolder = os.path.abspath(config["sourcepath"]);
        backUpspaceFolder = os.path.abspath(config["targetpath"]);
        Type = config["Type"];
        timeStep = config["CTime"] * 3600;
        Loop = config["Loop"];
        Ignore = config["Ignore"];

    except IOError:
        print 'can not load config'
        sys.exit()
    finally:
        if configFile != None:
            configFile.close();
    backUpspaceFolderflag = backUpspaceFolder
    if os.path.exists(backUpspaceFolder) == False:
        os.makedirs(backUpspaceFolder)

    if os.path.exists(WorkspaceFolder) == False:
        print WorkspaceFolder + ' no such dir'
        sys.exit()
    while (1):
        num = num + 1;
        if Loop > 0:
            print '--------------------the ' + str(num) + ' times of backup---------------------'
        main(WorkspaceFolder, backUpspaceFolder)
        if Loop > 0:
            print 'next back up is after ' + str(timeStep) + ' s';
            time.sleep(timeStep)
        else:
break;