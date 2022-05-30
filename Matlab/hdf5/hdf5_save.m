% Source: https://www.mathworks.com/help/matlab/import_export/export-to-hdf5-files.html;jsessionid=d59d230bed3467b29f4b19013d80
function hdf5_save(data, filename)

finalfilename = fullfile(pwd,filename);
fileID = H5F.create(finalfilename,'H5F_ACC_TRUNC','H5P_DEFAULT','H5P_DEFAULT');
datatypeID = H5T.copy('H5T_NATIVE_DOUBLE');
dims = size(data);
dataspaceID = H5S.create_simple(2,fliplr(dims),[]);
dsetname = 'my_dataset';  
datasetID = H5D.create(fileID,dsetname,datatypeID,dataspaceID,'H5P_DEFAULT');
H5D.write(datasetID,'H5ML_DEFAULT','H5S_ALL','H5S_ALL', 'H5P_DEFAULT',data);
H5D.close(datasetID);
H5S.close(dataspaceID);
H5T.close(datatypeID);
H5F.close(fileID);