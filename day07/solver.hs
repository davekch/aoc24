{-# LANGUAGE QuasiQuotes #-}

import Text.RawString.QQ 
import Data.List
import Utils
import AoC

getInput :: IO String
getInput = readFile "input.txt"

--------------------------------------------------------------------

type Parsed = [(Int, [Int])]
type Sol1 = Int
type Sol2 = Int

parse :: String -> Parsed
parse = map (\ns -> (head ns, tail ns)) . map parseInts . lines


check :: [Int -> Int -> Int] -> Int -> [Int] -> Bool
check ops test (n:ns) = check' test ns n
    where
        check' test [] acc = test == acc
        check' test (n:ns) acc
            | acc > test = False
            | otherwise = any (\op -> check' test ns (op acc n)) ops


solve1 :: Parsed -> Sol1
solve1 = sum . map fst . filter (uncurry (check [(+), (*)]))


concatInts :: Int -> Int -> Int
concatInts a b = read $ show a ++ show b


solve2 :: Parsed -> Sol2
solve2 = sum . map fst . filter (uncurry (check [(+), (*), concatInts]))


testdata = [r||]
testresult1 = 0
testresult2 = 0

--------------------------------------------------------------------

test1 = test (solve1 . parse) testresult1 testdata
test2 = test (solve2 . parse) testresult2 testdata

printPart :: (Show a) => Int -> a -> IO ()
printPart part solution = do
    putStr $ "Part " ++ (show part) ++ ": "
    print solution

main' :: CLIOptions -> IO ()
main' (CLIOptions p False) = do
    parsed <- parse <$> getInput
    case p of
        1 -> printPart 1 (solve1 parsed)
        2 -> printPart 2 (solve2 parsed)
        _ -> (do
            printPart 1 (solve1 parsed)
            printPart 2 (solve2 parsed))
main' (CLIOptions p True) = 
    case p of
        1 -> printPart 1 test1
        2 -> printPart 2 test2
        _ -> (do
            printPart 1 test1
            printPart 2 test2)

main = main' =<< clioptions
