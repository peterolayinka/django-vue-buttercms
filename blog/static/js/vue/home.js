// The ButterCMS token has been removed for security reasons.

const butter = Butter(butterToken);
const { createApp, h, component } = Vue;

const app = createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      message: "Hello Vue!",
      page: {},
    };
  },
  methods: {
    getPageFields() {
      const fields = this.page.fields;
      return fields && fields.body;
    },
  },
  mounted() {
    butter.page
      .retrieve("*", "landing-page-with-components")
      .then((response) => (this.page = response.data.data));
  },
});

// register an options object
app.component("render-element", {
  props: ["fields"],
  template: `
    <div
        v-for="(element, index) in fields"
        :key="index"
        :class="{
          'hero': element.type === 'hero',
          'two_column_with_image' : element.type === 'two_column_with_image',
          'features': element.type === 'features',
          'testimonials': element.type === 'testimonials',
        }"
      >
      <div class="hero-wrapper" v-if="element.type == 'hero'" :style="{
        'background': 'url('+element.fields.image+')',
        'background-repeat': 'no-repeat',
        'background-size': '100% 100%',
      }">
        <div class="container" >
        <h1>{{ element.fields.headline }}</h1>
        <p>{{ element.fields.subheadline }}</p>
        <a :href="element.fields.button_url" class="btn">{{ element.fields.button_label }}</a>
        </div>
      </div>
      <div class="container" v-if="element.type == 'two_column_with_image'">
        <div v-if="element.fields.image_position === 'left'" :style="{
          'background': 'url('+element.fields.image+')',
          'background-repeat': 'no-repeat',
          'background-size': '100% 100%',
        }">
        </div>
        <div>
          <h2>{{ element.fields.headline }}</h2>
          <div v-html="element.fields.subheadline"></div>
          <a :href="element.fields.button_url" class="btn">{{ element.fields.button_label }}</a>
        </div>
        <div v-if="element.fields.image_position === 'right'" :style="{
          'background': 'url('+element.fields.image+')',
          'background-repeat': 'no-repeat',
          'background-size': '100% 100%',
        }">
        </div>
      </div>
      <div class="container" v-if="element.type == 'features'">
        <h2>{{ element.fields.headline }}</h2>
        <p>{{ element.fields.subheadline }}</p>
        <div class="feature-item">
          <div v-for="(feature, index) in element.fields.features" :key="index">
            <div class="feature">
              <div class="icon">
                <img :src="feature.icon" />
              </div>
              <div class="text">
                <h3>{{ feature.headline }}</h3>
                <p>{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="container" v-if="element.type == 'testimonials'">
        <h2>{{ element.fields.headline }}</h2>
        <div class="testimonial-item">
          <div v-for="(testimonial, index) in element.fields.testimonial" :key="index">
            <div class="testimonial">
              <div class="quote">
                <p>{{ testimonial.quote }}</p>
              </div>
              <div class="author">
                <p>{{ testimonial.name }} (<span>{{ testimonial.title }}</span>)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    `,
});

app.mount("#butter-page");
