% Transtion Matrix
a = [0.5, 0.5, 0, 0;
    0,   0.7, 0.3, 0;
    0, 0, 0.8, 0.2;
    0, 0, 0,1];
% markov chain
mc = dtmc(a,'StateNames',["State 1" "State 2" "State 3" "State 4"]);
figure;
graphplot(mc,'ColorNodes',true,'ColorEdges',true)