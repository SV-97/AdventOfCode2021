import Data.List (unfoldr, foldl')
import Data.Bifunctor (first, second)

type Fold = (Char, Int)
type Coord = (Int, Int)
data Grid = Grid { height :: Int, width :: Int , ones :: [Coord]} deriving (Show, Eq)

toGrid :: [Coord] -> Grid
toGrid coords = Grid {height=h + 1, width=w + 1, ones=coords}
    where
        w = maximum $ map fst coords
        h = maximum $ map snd coords

splitAtChar :: Char -> String -> [String]
splitAtChar c = unfoldr f
    where
        f [] = Nothing
        f l  = Just . fmap (drop 1) . break (== c) $ l

removeCol :: Int -> Grid -> Grid
removeCol idx grid = grid{width = width grid - 1, ones=o1 ++ o2}
    where 
        o1 = filter ((< idx). fst) $ ones grid
        o2 = map (\(x,y) -> (x,y-1)) $ filter ((>idx). fst) $ ones grid

removeRow :: Int -> Grid -> Grid
removeRow idx grid = grid{height = height grid - 1, ones=o1 ++ o2}
    where
        o1 = filter ((< idx). snd) $ ones grid
        o2 = map (\(x,y) -> (x,y-1)) $ filter ((>idx). snd) $ ones grid

removeMiddleCol ::Grid -> Grid
removeMiddleCol grid = removeCol (width grid `div` 2) grid

removeMiddleRow :: Grid -> Grid
removeMiddleRow grid = removeRow (height grid `div` 2) grid

foldAlongY :: Grid -> Grid
foldAlongY grid
    | even (width grid) = leftHalf{ones = (ones leftHalf) ++ (ones rightHalf)}
    | otherwise = error "Tried calling foldAlongX with odd width."
    where
        w = width grid
        hw = w `div` 2
        leftHalf = grid{width=hw, ones=o1}
        o1 = filter ((<hw) . fst) $ ones grid
        rightHalf = grid{width=hw, ones=o2}
        o2 = map (first (w-)) $ filter ((>=hw) . fst) $ ones grid


foldAlongX :: Grid -> Grid
foldAlongX grid
    | even (height grid) = upperHalf{ones = (ones upperHalf) ++ (ones lowerHalf)}
    | otherwise = error "Tried calling foldAlongX with odd height."
    where
        h = height grid - 1
        hh = height grid `div` 2
        upperHalf = grid{height=hh, ones=o1}
        o1 = filter ((<hh) . snd) $ ones grid
        lowerHalf = grid{height=hh, ones=o2}
        o2 = map (second (h-)) $ filter ((>=hh) . snd) $ ones grid

applyFold :: Fold -> Grid -> Grid
applyFold f@('x', idx) grid
    | odd (width grid) = applyFold f $ removeMiddleCol grid -- removeCol idx grid
    | otherwise = foldAlongY grid
applyFold f@('y', idx) grid
    | odd (height grid) = applyFold f $ removeMiddleRow grid -- removeRow idx grid
    | otherwise = foldAlongX grid
applyFold f@(c, idx) grid = error $ "Can't applyFold along axis" ++ [c]

showGrid :: Grid -> String 
showGrid g = mconcat [row y ++ "\n" | y <- [0..height g - 1]]
    where
        row :: Int -> String
        row y = [charAt x y | x <- [0..width g - 1] ]
        charAt :: Int -> Int -> Char
        charAt x y
            | (x,y) `elem` ones g = '█'
            | otherwise = ' '

s = putStrLn . showGrid
main = do
    coordLines <- lines <$> readFile "input.txt"
    let coords = map ((\[x,y] -> (read x, read y)) . splitAtChar ',') coordLines :: [Coord]
    let grid = toGrid coords
    foldLines <- lines <$> readFile "input2.txt"
    let folds = map ((\[x,y] -> (last x, read y)) . splitAtChar '=') foldLines :: [Fold]
    -- print folds
    let result = foldl' (flip applyFold) grid folds
    print grid -- $ applyFold (head folds) grid
    putStrLn $ showGrid result