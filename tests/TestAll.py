from tradingpatterns.hard_data import generate_sample_df_with_pattern
from tradingpatterns.tradingpatterns import detect_patterns, plot_patterns

def test_detect_patterns():
    # Generate data with different patterns
    df_head_shoulder = generate_sample_df_with_pattern("Head and Shoulder")
    df_inv_shoulder = generate_sample_df_with_pattern("Inverse Head and Shoulder")
    df_double_top = generate_sample_df_with_pattern("Double Top")
    df_double_bottom = generate_sample_df_with_pattern("Double Bottom")
    df_triple_top = generate_sample_df_with_pattern("Triple Top")
    df_triple_bottom = generate_sample_df_with_pattern("Triple Bottom")

    plot_patterns(df_head_shoulder)
    plot_patterns(df_inv_shoulder)
    plot_patterns(df_double_top)
    plot_patterns(df_double_bottom)
    plot_patterns(df_triple_top)
    plot_patterns(df_triple_bottom)


    # Detect patterns
    df_with_head_shoulder_detection = detect_patterns(df_head_shoulder)
    df_with_inv_shoulder_detection = detect_patterns(df_inv_shoulder)
    df_with_double_top_detection = detect_patterns(df_double_top)
    df_with_double_bottom_detection = detect_patterns(df_double_bottom)
    df_with_triple_top_detection = detect_patterns(df_triple_top)
    df_with_triple_bottom_detection = detect_patterns(df_triple_bottom)

    # Assert that the detected patterns are present in the respective DataFrames
    assert "Head and Shoulder" in df_with_head_shoulder_detection['head_shoulder_pattern'].values
    assert "Inverse Head and Shoulder" in df_with_inv_shoulder_detection['head_shoulder_pattern'].values
    assert "Double Top" in df_with_double_top_detection['pattern'].values
    assert "Double Bottom" in df_with_double_bottom_detection['pattern'].values
    assert "Triple Top" in df_with_triple_top_detection['pattern'].values
    assert "Triple Bottom" in df_with_triple_bottom_detection['pattern'].values

#Now you should modify the detect_patterns function in the tradingpatterns.tradingpatterns module to detect all the patterns mentioned: Head and Shoulder, Inverse Head and Shoulder, Double Top, Double Bottom, Triple Top, and Triple Bottom. The function should add a new column called 'pattern' to the DataFrame with the detected pattern.