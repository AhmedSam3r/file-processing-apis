- [x] run initial flask app
- [x] create initial empty routes for image operations
  - [x] upload
  - [x] return random line
  - [x] return reverse random line
  - [x] return 20 longest lines of a file
  -  [x] return 100 longest lines of a file
- [x] create middleware for these apis to check content header
- [x] implement the upload api
  - [x] consider filesize
- [x] implement the return random line in the previous file upload api
  - [x] consider using seed method to randomize the line
  - [] consider the file size & # of lines 
- [x] implement the return 20 longest lines of a certain file
  - [x] s
- [x] implement the return 100 longest lines of all files
  - [x] s
- [ ] Create 
  - [ ] Dockerfile
  - [ ] docker-compose.yml
- [ ] Refactor the app in the following parts
  - [ ] fix the abort method
  - [ ] implement task queue
  - [ ] move the file processing asyncronosly in the background
- [] Update the docker-compose.yml file

- [ ] setup the testing using pytest 
  - [ ] create different scenarios for upload
  - [ ] create different scenarios for longest random file lines
  - [ ] create different scenarios for longest 20 lines
  - [ ] - [ ] create different scenarios for longest 100 lines