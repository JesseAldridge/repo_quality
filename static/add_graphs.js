function add_graphs(repo_list) {
  repo_list.forEach(function(repo_obj, index) {
    var data_objs = [];

    var iso_dt_to_score = repo_obj.timestamp_to_score;

    console.log('adding graph:', iso_dt_to_score);

    Object.keys(iso_dt_to_score).forEach(function(iso_dt) {
      data_objs.push({
        timestamp: new Date(Date.parse(iso_dt)),
        value: iso_dt_to_score[iso_dt],
      });
    });

    data_objs.sort(function(a, b) {
      return a.timestamp > b.timestamp ? 1 : -1
    });

    time_series(data_objs, '#repo-' + index);
  });
};
