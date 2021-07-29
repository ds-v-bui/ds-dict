<template>
    <div>
        <Search
            :has-results="data.length > 0"
            :is-searching="isSearching"
            @search="search">
        </Search>
        <div>
            <Word
                :key="word.id"
                :word="word"
                v-for="word in data"
            />
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Search from "./Search";
    import Word from "./pages/Word";

    export default {
        name: "Home",

        components: {
            Search,
            Word
        },

        data: () => ({
            settings: {},
            data: [],
            isSearching: false
        }),

        methods: {
            async search(settings) {
                this.isSearching = true;
                this.data = [];
                this.settings = JSON.parse(JSON.stringify(settings.api));

                if (this.settings.query !== '') {
                    if (this.settings.type === 'vn-ja'){
                        await axios.get(
                            this.$hostname
                            + '/api/search/vidictionary?vi_text='
                            + encodeURIComponent(this.settings.query)
                        ).then(response => {
                            this.data = response.data;
                        }).catch(e => {
                            alert(e.message);
                        });
                    } else {
                        await axios.get(
                            this.$hostname
                            + '/api/search/jadictionary?ja_text='
                            + encodeURIComponent(this.settings.query)
                        ).then(response => {
                            this.data = response.data;
                        }).catch(e => {
                            alert(e.message);
                        });
                    }
                } else
                    this.data = [];

                this.isSearching = false;
            }
        }
    }
</script>

<style scoped lang="scss">
    .md-icon-button {
        position: absolute;
        right: calc(5% - 20px);
        top: 90px;
    }

    @media screen and (max-width: 768px) {
        .md-icon-button {
            position: relative;
            left: calc(50% - 20px);
            top: -20px;
        }
    }
</style>
