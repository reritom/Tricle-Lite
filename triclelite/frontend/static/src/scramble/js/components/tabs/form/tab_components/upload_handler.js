export default {
  name: "UploadHandler",
  data: function () {
    return {
      uploadFieldName: "Photos",
      ourFileList: []
    }
  },
  template: `<div>
              <div class="dropbox">
                <input class="input-file" type="file" multiple :name="uploadFieldName" @change="filesChange($event.target.name, $event.target.files)"  accept="image/*">
                <p v-if="isInitial">
                  Drag your file(s) here to begin<br> or click to browse
                </p>
                <p v-else>
                  Add some more files if you want
                </p>
              </div>
              <button @click="removeAll()">Remove all selected files</button>
              <div class="flex-container-row-ns">
              <div class="box-preview" v-for="file, index in ourFileList" @click="removeOne(index)">
              Deselect {{file.name}}
              </div>
              </div>
            </div>`,
  methods: {
    filesChange: function(fieldName, fileList) {
      // To handle new images being selected
      if (this.ourFileList.length === 0){
        this.ourFileList = Array.prototype.slice.call(fileList);
      }
      else {
        // We merge any of the unique files added
        console.log(typeof(fileList));
        console.log(fileList);
        this.ourFileList = this.mergeObjects(this.ourFileList, fileList);
      }
    },
    mergeObjects: function(first, second) {
      // This method merges a list (first) with a filelist (second) to make a list with no duplicates
      var third = [];

      // Create a list for each
      var first_list = Array.prototype.slice.call(first);
      var second_list = Array.prototype.slice.call(second);

      // Create a list with the existing file names
      var existing_filenames = []
      for (var i = 0; i < first_list.length; i++) {
        existing_filenames.push(first_list[i].name);
      }

      console.log(first_list);
      console.log(second_list);

      // Merge the lists
      var third = first_list.concat(second_list.filter(function (item) {
          // For each of the new files name, if it is in the existing filename list, filter it.
          // Then concat the existing file list, with the filtered new list
          return existing_filenames.indexOf(item.name) < 0;
      }));

      return third
    },
    removeAll: function() {
      // Remove all selected files
      this.ourFileList = [];
    },
    removeOne: function(index) {
      // Remove a single selected file based on its index
      Vue.delete(this.ourFileList, index);
    }
  },
  watch: {
    ourFileList() {
      this.$emit('filesadded', this.ourFileList)
    }
  },
  computed: {
    isInitial() {
      return this.ourFileList.length === 0
    }
  }
};
