% script anydouble checks where there are any numbers double in any row,
% column or box

double = 0;


for i=1:9 % indexing over numbers from 1 to 9
    
    for j=1:9% indexing over rows 1 to 9
        I=find(board(j,:) == i);
        if length(I)>1
            double = 1;
            break
        end
    end
    
    if double
        break
    end
    
    for j=1:9% indexing over columns 1 to 9
        I=find(board(:,j) == i);
        if length(I)>1
            double = 1;
            break
        end
    end
    
    if double
        break
    end
    
    for j=1:9 % building boxes
        box = board(1+3*mod(j,3):1+3*mod(j,3)+2,1+3*floor((j-1)/3):1+3*floor((j-1)/3)+2);
        vec = [box(1,:),box(2,:),box(3,:)];
        I=find(vec == i);
        if length(I)>1
            double = 1;
            break
        end
    end
    
    if double
        break
    end
    
end

