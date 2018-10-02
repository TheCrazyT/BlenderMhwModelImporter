{
    "package": {
        "name": "BlenderMhwModelImporter",
        "repo": "BlenderMhwModelImporter",
        "subject": "thecrazyt",
        "vcs_url": "https://travis-ci.org/TheCrazyT/BlenderMhwModelImporter",
        "licenses": ["MIT"]
    },

    "version": {
        "name": "0.6"
    },

    "files":
        [
            {
                "includePattern": "/home/travis/build/TheCrazyT/BlenderMhwModelImporter/build/(.*)/(.*)", "uploadPattern": "$1/$2",
                "matrixParams": {
                    "override": 1 
                }
            }
        ],
    "publish": true
}
