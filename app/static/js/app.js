$(document).foundation()

// Dropzone has been added as a global variable.
// const dropzone = new Dropzone("div.my-dropzone", { url: "/file/post" });

Dropzone.options.uploaddropzone = { // The camelized version of the ID of the form element
    // Configuration options go here
    autoProcessQueue: false,
    uploadMultiple: false,
    parallelUploads: 10,
    maxFiles: 5,
    addRemoveLinks: true,
    maxFilesize: 512,
    acceptedFiles: ".mov,.mp4,.conf,.pdf",


    // The setting up of the dropzone
    init: function() {
        var myDropzone = this;

        // First change the button to actually tell Dropzone to process the queue.
    this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
        // Make sure that the form isn't actually being sent.
        e.preventDefault();
        e.stopPropagation();
        myDropzone.processQueue();
      });

      // Listen to the success event, whenever upload completion success fired, previewElement
      // file thumbnail container will be removed. with 3s delay
      this.on("success", function(files, response){
        //setTimeout(() => { files.previewElement.remove(); }, 3000);
        setTimeout(() => { this.removeFile(files); }, 3000);
      }
      );

      // placeholder for custom error message
      // this.on("error", function(file, message) {
      //   $(file.previewElement).find('.dz-error-message').text(message.Message);
      // });

      // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
      // of the sending event because uploadMultiple is set to true.
      this.on("sendingmultiple", function() {
        // Gets triggered when the form is actually being sent.
        // Hide the success button or the complete form.
      });
      this.on("successmultiple", function(files, response) {
        // Gets triggered when the files have successfully been sent.
        // Redirect user or notify of success.
      });
      this.on("errormultiple", function(files, response) {
        // Gets triggered when there was an error sending the files.
        // Maybe show form again, and notify user of error
      });
    }
  }
