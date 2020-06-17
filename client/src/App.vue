<template>
  <div>
    <select v-model="selectedForm">
      <option :value="f" v-for="f in forms">{{f}}</option>
    </select>
    <button v-if="htmlForm" @click="onDownloadClick">Download</button>
    <component ref="htmlFormComponent" v-if="htmlForm" :is="formComponent"></component>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedForm: null,
      htmlForm: null,
      forms: []
    };
  },
  created() {
    axios("/api/form").then(response => (this.forms = response.data.forms));
  },
  watch: {
    selectedForm() {
      axios(`/api/form/${this.selectedForm}`).then(response => {
        let html = response.data.html.replace(
          /\{\{(\w+)\}\}/g,
          '<input ref="$1" placeholder="$1">'
        );
        this.htmlForm = html;
      });
    }
  },
  computed: {
    formComponent() {
      return {
        template: `<div>${this.htmlForm}</div>`
      };
    }
  },
  methods: {
    onDownloadClick() {
      let data = this.$refs.htmlFormComponent.$refs;
      let params = Object.keys(data)
        .map(function(key) {
          return [key, data[key].value].map(encodeURIComponent).join("=");
        })
        .join("&");
      let url = `/api/form/print/${this.selectedForm}?${params}`;
      window.open(url);
    }
  }
};
</script>