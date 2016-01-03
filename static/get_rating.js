
function get_rating(repo_obj) {
  var score = repo_obj.score;
  var rating = '', explanation = '';
  if(score > 4000) {
    rating = 5;
    explanation = 'Outstanding!'
  }
  else if(score > 1000) {
    rating = 4;
    explanation = 'Good'
  }
  else if(score > 400) {
    rating = 3;
    explanation = 'Ok'
  }
  else if(score > 200) {
    rating = 2;
    explanation = 'Bad'
  }
  else if(score > 100) {
    rating = 1;
    explanation = 'Terrible'
  }
  else
    return '💩';
  rating_str = ''
  for(var i = 0; i < rating; i++)
    rating_str += '⭐️' + ' '
  return rating_str + '  ' + explanation
}
